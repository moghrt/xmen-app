<template>
  <q-page class="constrain q-pa-md">
    <div>
      <!----<home-stories></home-stories>
            <newsfeed></newsfeed> -->
    </div>
    <div class="row q-col-gutter-lg">
      <div class="col-sm-8 col-12">
        <q-card class="card-post q-mb-md" flat bordered v-for="post in posts" :key="post.id">
          <q-item>
            <q-item-section avatar>
              <router-link :to="`/profile/${post.user_id}`">
                <q-avatar>
                  <img :src="post.user_avatar_url">
                </q-avatar>
              </router-link>
            </q-item-section>
            <q-item-section>
              <q-item-label>
                <span class="text-bold">{{ post.user_name }}</span>
                <span class="text-grey-13 q-px-sm">{{ dateSerialized(post.created_at) }}</span>
              </q-item-label>
              <q-item-label caption>
                {{ post.user_caption }}
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-separator />
          <q-card-section>
            <q-img :src="post.image" />
            <q-btn-group outline class="q-mt-sm" v-if="!isMyPost(post)">
              <q-btn outline padding="xs" :color="postLikeStatus(post).color" :icon="postLikeStatus(post).icon"
                @click="buttonLike(post)" />
            </q-btn-group>
            <div v-if="post.likes > 0" class="text-bold q-mt-sm">{{ post.likes }} Me gusta</div>
            <div class="q-mt-sm"><span class="text-bold">{{ post.user_name }}</span> {{ post.title }}</div>
            <q-expansion-item class="no-padding" v-show="post.description.length > 0" hide-expand-icon icon="">
              <template v-slot:header="{ expanded }">
                <q-item-section class="text-grey-13">
                  {{ expanded ? '... menos' : '... mas' }}
                </q-item-section>
              </template>
              <q-card>
                <p class="pre-line">
                  {{ post.description }}
                </p>
              </q-card>
            </q-expansion-item>
            <div class="q-mt-md" v-if="post.number_of_comments > 0">
              <q-btn flat padding="xs" class="text-grey-13 comments" @click="postDetail(post.id)">ver los {{
                post.number_of_comments
                }} comentarios</q-btn>
            </div>
            <form>
              <q-input bottom-slots v-model="commentInput[post.id]" placeholder="Añade un comentario" dense>
                <template v-slot:append>
                  <q-icon v-if="commentInput[post.id] != null" name="close" @click="commentInput[post.id] = null"
                    icon="eva-close-outline" />
                  <q-btn v-if="commentInput[post.id] != null" round dense flat icon="eva-checkmark-circle-outline"
                    @click="sendComment(post)" type="submit" />
                </template>
              </q-input>
            </form>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-4 large-screen-only">
        <q-card class="card-profile fixed">
          <component-user-resume :toUrl="dataComponent.to_url" :avatarUrl="dataComponent.avatar_url"
            :name="dataComponent.name" :caption="dataComponent.caption"></component-user-resume>
        </q-card>
      </div>
    </div>
    <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
      <q-btn fab icon="keyboard_arrow_up" color="primary" />
    </q-page-scroller>
  </q-page>
</template>

<script>
import { computed, ref } from 'vue';
import { api } from 'boot/axios'
import { authStore } from 'stores/store';
import { storeToRefs } from 'pinia'
import ComponentUserResume from 'src/components/ComponentUserResume.vue';
export default {
  name: 'PageHome',
  components: {
    ComponentUserResume
  },
  setup() {
    const store = authStore();
    return {
      store,
    };
  },
  data() {
    return {
      // Usa ref para que sea reactivo, pavo.
      dataComponent: ref({
        to_url: `/profile/${this.store.user_id}`,
        avatar_url: this.store.user_avatar_url,
        name: this.store.user_name,
        caption: this.store.user_caption,
      }),
      posts: [],
      nextPage: 1,
      hasNext: false,
      likeIcon: {
        icon: 'eva-heart-outline',
        color: 'primary',
      },
      commentInput: [],
    };
  },
  computed: {
  },
  mounted() {
    this.loadPosts();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    loadPosts() {
      if (this.nextPage == null)
        return;

      api.post(`/api/v1/posts/get_posts/?page=${this.nextPage}`, { 'user_id': this.store.user_id })
        .then(response => {
          this.hasNext = false;
          if (response.data.next)
            this.hasNext = true;
          // Los posts vienen paginados desde django. Voy incrementando la lista de post cada vez que llego al final de la misma.
          for (let i = 0; i < response.data.results.length; i++) {
            this.posts.push(response.data.results[i]);
          }
        })
    },
    postDetail(post_id) {
      this.$router.push(`/post/${post_id}`);
    },
    dateSerialized(dateTime) {
      const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' };
      return new Date(dateTime).toLocaleDateString('es-Es', options);
    },
    isMyPost(post) {
      if (post.user_id === this.store.user_id.toString()) {
        // Son mis posts. No muestro las opciones de interacción de los posts.
        return true;
      }
    },
    buttonLike(post) {
      let data = {
        post_id: post.id,
        user_id: this.store.user_id,
      };
      if (post.liked_by_me) {
        this.unlikePost(data);
        post.liked_by_me = false;
        post.likes--;
      }
      else {
        this.likePost(data);
        post.liked_by_me = true;
        post.likes++;
      }
    },
    likePost(data) {
      // Dar like al post.
      api.post(`/api/v1/likes/create_like/`, data)
        .then(response => {
          if (response.status = 201) {
          }
        })
        .catch(error => {
          console.log(error.data);
        });
    },
    unlikePost(data) {
      // Quitar like al post.
      api.post(`/api/v1/likes/destroy_like/`, data)
        .then(response => {
          if (response.status = 201) {
          }
        })
        .catch(error => {
          console.log(error.data);
        });
    },
    postLikeStatus(post) {
      if (post.liked_by_me == true) {
        return { icon: 'eva-heart', color: 'secondary' };
      }
      else
        return { icon: 'eva-heart-outline', color: 'primary' };

    },
    handleScroll() {
      let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      if (bottomOfWindow && this.hasNext) {
        this.nextPage++;
        this.loadPosts();
      }
    },
    sendComment(post) {
      // Enviar un comentario.
      if(this.commentInput[post.id].trim().length == 0){
        return;
      }

      let data = {
        'post_id': post.id,
        'comment': this.commentInput[post.id],
        'user_id': this.store.user_id,
      };
      console.log(data);
      api.post(`/api/v1/comments/create_comment/`, data)
        .then(response => {
          if (response.status = 201) {
            this.commentInput[post.id] = null;
            post.number_of_comments++;
          }
        })
        .catch(error => {
          console.log(error.data);
        });
    }
  },
};
</script>

<style>
.card-post .q-img {
  min-height: 200px;
}

.no-padding .q-item {
  padding: 0;
}

.q-focus-helper {
  background: inherit;
  opacity: 1;
}

a.comments {
  text-decoration: none
}

a.comments:hover {
  text-decoration: underline
}

.q-btn--outline:before {
  border: none;
}

.q-field__native,
.q-field__prefix,
.q-field__suffix,
.q-field__input {
  color: #4f4f4f;
}
</style>
