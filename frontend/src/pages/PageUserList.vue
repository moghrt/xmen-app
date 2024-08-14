<template>
  <q-page class="constrain q-pa-md">
    <div class="row q-col-gutter-lg">
      <div class="col-sm-8 col-12">
        <q-input v-model="userSearch" label="Buscar usuario" dense clearable />
      </div>
      <div class="col-sm-8 col-12">
        <q-scroll-area class="vh-65">
          <q-card class="card-post q-mb-xs" flat bordered v-for="user in filteredItems" :key="user.id">
            <q-item>
              <q-item-section avatar>
                <router-link :to="`/profile/${user.id}`">
                  <q-avatar>
                    <img :src="user.avatar_url">
                  </q-avatar>
                </router-link>
              </q-item-section>
              <q-item-section>
                <q-item-label>
                  <span class="text-bold">{{ user.name }}</span>
                </q-item-label>
                <q-item-label caption>
                  {{ user.caption }}
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-card>
        </q-scroll-area>
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
  name: 'PageUserList',
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
      data: [],
      nextPage: 0,
      hasNext: false,
      likeIcon: {
        icon: 'eva-heart-outline',
        color: 'primary',
      },
      commentInput: [],
      userSearch: '',
    };
  },
  computed: {
    filteredItems() {
      let query = this.userSearch ? this.userSearch.toLowerCase() : '';
      return this.data.filter(item =>
        item.name.toLowerCase().includes(query)
      );
    },
  },
  mounted() {
    this.loadUsers();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    createOrJoinRoom(userId){
      //Si ya existe la sala de chat, nos unimos a ella. Si no, se crea una con el id de ambos usuarios.
      console.log("createOrJoinRoom: " + this.store.user_id + " " + userId);
    },
    loadUsers() {
      api.post(`/api/v1/users/get_users/`)
        .then(response => {
          this.data = response.data;
        })
    },
    loadUsersPaginated() {
      if (this.nextPage == null)
        return;

      let data = {
        'page': this.nextPage,
      };

      api.post(`/api/v1/users/get_users?paginated/`, data)
        .then(response => {
          this.hasNext = false;
          if (response.data.next)
            this.hasNext = true;
          // Los posts vienen paginados desde django. Voy incrementando la lista de post cada vez que llego al final de la misma.
          for (let i = 0; i < response.data.results.length; i++) {
            this.data.push(response.data.results[i]);
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
    handleScroll() {
      let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      if (bottomOfWindow && this.hasNext) {
        this.nextPage++;
        this.loadUsers();
      }
    },
    sendComment(post) {
      // Enviar un comentario.
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
