<template>
  <q-page class="constrain q-pa-md container">
    <div class="col-sm-8 col-12">
      <q-scroll-area class="vh-70" ref="scrollArea" horizontal-bar-style="{display: none}">
        <q-card class="card-post q-mb-md" flat bordered>
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
            <q-img id="post-image" :src="post.image" />
            <q-btn-group outline class="q-mt-sm">
              <q-btn outline padding="xs" v-if="!isMyPost(post)" :color="postLikeStatus(post).color"
                :icon="postLikeStatus(post).icon" @click="buttonLike(post)" />
            </q-btn-group>
            <div v-if="post.likes > 0" class="text-bold q-mt-sm">{{ post.likes }} Me gusta</div>
            <div class="q-mt-sm"><span class="text-bold">{{ post.user_name }}</span> {{ post.title }}</div>
            <div id="post-description" class="q-mt-sm">
              <p class="pre-line">
                {{ post.description }}
              </p>
            </div>
            <div id="post-comments">

              <div class="q-mt-md" v-for="comment in post.comments" :key="comment.id">
                <q-item class="comment">
                  <q-item-section avatar>
                    <router-link :to="`/profile/${comment.user_id}`">
                      <q-avatar>
                        <img :src="comment.user_avatar_url">
                      </q-avatar>
                    </router-link>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>
                      <span class="text-bold">{{ comment.user_name }}:</span>
                      <span class="q-px-sm">{{ comment.text }}</span>
                    </q-item-label>
                    <q-item-label caption>
                      {{ dateSerialized(comment.created_at) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </q-scroll-area>
    </div>
    <div class="col-4 large-screen-only">
      <q-card class="card-profile fixed">
        <component-user-resume :toUrl="dataComponent.to_url" :avatarUrl="dataComponent.avatar_url"
          :name="dataComponent.name" :caption="dataComponent.caption"></component-user-resume>
      </q-card>
    </div>
    <div class="q-py-sm">
      <q-form class="q-gutter-md">
        <q-input bottom-slots v-model="commentInput" placeholder="Añade un comentario" dense
          :rules="[val => val != null && !!val.trim() || 'El campo no puede estar vacio.']">
          <template v-slot:append>
            <q-icon v-if="commentInput != null" name="close" @click="commentInput = null" icon="eva-close-outline" />
            <q-btn v-if="commentInput != null && !!commentInput.trim()" round dense flat icon="eva-checkmark-circle-outline"
              @click="sendComment(commentInput)" type="submit" />
          </template>
        </q-input>
      </q-form>
    </div>
    <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
      <q-btn fab icon="keyboard_arrow_up" color="primary" />
    </q-page-scroller>
  </q-page>
</template>

<script>
import { ref } from 'vue';
import { api } from 'boot/axios'
import { authStore } from 'stores/store';
import ComponentUserResume from 'src/components/ComponentUserResume.vue';
export default {
  name: 'PageHome',
  components: {
    ComponentUserResume
  },
  setup() {
    const store = authStore();
    return { store };
  },
  data() {
    return {
      dataComponent: ref({
        to_url: `/profile/${this.store.user_id}`,
        avatar_url: this.store.user_avatar_url,
        name: this.store.user_name,
        caption: this.store.user_caption,
      }),
      post: [],
      nextPage: 1,
      hasNext: false,
      likeIcon: {
        icon: 'eva-heart-outline',
        color: 'primary',
      },
      commentInput: null,
      openPopUpComment: false,
      windowHeight: (window.innerHeight * 3) / 4,
      scrollAreaHeigth: ref(0),
      scrollAreaIncrement: 46,
    };
  },
  computed: {
    customStyle() {
      return {
        height: screen.height,
      }
    }
  },
  mounted() {
    this.loadPost(true);
    //window.addEventListener('scroll', this.handleScroll);
    //window.addEventListener('resize', this.onResize)
  },
  /*beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },*/
  methods: {
    animateScroll() {
      const duration = 1; // ms - usa 0 para scoll instanténeo.
      this.calculateHeight();
      this.$refs.scrollArea.setScrollPosition('vertical', this.scrollAreaHeigth, duration);
    },
    calculateHeight() {
      var image = document.getElementById('post-image');
      var description = document.getElementById('post-description');
      var comments = document.getElementById('post-comments');

      this.scrollAreaHeigth += image.offsetHeight + description.offsetHeight + comments.offsetHeight;
    },
    loadPost(init) {
      if (this.nextPage == null)
        return;

      // Si no añadimos la página, cargamos todos de una vez.
      let data = {
        'user_id': this.store.user_id,
        'post_id': this.$route.params.id,
        //'page': this.nextPage,
      };

      api.post(`/api/v1/posts/detail_post/`, data)
        .then(response => {
          // Si es la primera pagina la que visito, cargo todo según viene.
          // Luego vamos añadiendo los comentarios según vayamos necesitando ver más.
          if (init) {
            this.post = response.data;
            this.hasNext = true;  // Marco que se puede cargar al hacer scroll.
          }
          else {
            this.loadPaginatedComments(response.data.comments);
          }
          if (this.post.comments_total == this.post.comments.length)
            this.hasNext = false;
        })
    },
    loadPaginatedComments(comments) {
      for (let i = 0; i < comments.length; i++) {
        this.post.comments.push(comments[i]);
        this.scrollAreaHeigth += this.scrollAreaIncrement;
      }
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
        this.loadPost(false);
      }
    },
    sendComment(scope) {
      // Enviar un comentario.
      let data = {
        'post_id': this.$route.params.id,
        'comment': scope,
        'user_id': this.store.user_id,
      };
      //scope.set();
      //this.scrollToBottom();

      api.post(`/api/v1/comments/create_comment/`, data)
        .then(response => {
          if (response.status = 201) {
            this.commentInput = '';
            this.openPopUpComment = false;
            //this.post.comments.unshift(response.data);  // Para añadir al principio.
            this.post.comments.push(response.data);  // Para añadir al principio.
            this.animateScroll();
          }
        })
        .catch(error => {
          console.log(error.data);
        });

    },
    /*scrollToBottom() {
      window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);
    },*/
    /*onResize() {
      console.log("On resize: " + window.innerHeight);
      this.windowHeight = window.innerHeight
    },*/
    /*onScroll(position) {
      if (position.verticalPercentage > 0.9 && this.hasNext) {
        console.log("dale");
        this.nextPage++;
        this.loadPost(false);
      }
      console.log(position);
    }*/
  },
};
</script>

<style>
.q-page-container {
  overflow: hidden;
}

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

.q-item.comment {
  padding: 0;

}

.comment-input {
  width: 100%;
  max-width: 100%;
}

.container {
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.scrollable {
  flex: 1
}

.sticky {
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
}

.q-scrollarea__content.absolute {
  width: 100%;
}
</style>
