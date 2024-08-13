<template>
  <q-page class="constrain q-pa-md">
    <div class="row q-col-gutter-lg col-12">
      <div class="col-12">
        <q-card class="my-card" flat bordered>
          <q-card-section horizontal>
            <q-card-section class="col-5 flex flex-center">
              <q-avatar size="120px">
                <img :src="userData.avatar_url">
              </q-avatar>
            </q-card-section>
            <q-card-section class="q-pt-xs vertical-center">
              <div class="text-h5 q-mt-sm q-mb-xs">{{ userData.name }}</div>
              <div class="text-caption text-grey">{{ userData.caption }}</div>
            </q-card-section>
          </q-card-section>
          <q-separator />
          <q-card-actions>
            <span class="q-pl-md text-grey-13"><b>{{ userData.number_of_posts }}</b> {{ postText }}</span>
          </q-card-actions>
        </q-card>
      </div>
    </div>
    <div class="row q-mt-sm q-col-gutter-xs full-width items-center content-center">
      <div class="col-md-4 col-6 text-center" v-for="post in posts" :key="post.id">
        <q-card class="card-post q-mb-md full-width image-container" flat>
          <router-link :to="`/post/${post.id}`">
            <q-img class="img-thumbnail" :src="post.image" />
          </router-link>
        </q-card>
      </div>
    </div>
    <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
      <q-btn fab icon="keyboard_arrow_up" color="primary" />
    </q-page-scroller>
  </q-page>
</template>

<script>
import { api } from 'boot/axios'
import { authStore } from 'stores/store';
export default {
  name: "PageProfile",
  setup() {
    const store = authStore();
    return {
      store
    };
  },
  data() {
    return {
      posts: [],
      userData: {
        id: '',
        name: '',
        caption: '',
        avatar_url: '',
        number_of_posts: '',
      },
      hasNext: false,
      nextPage: 1,
      postText: ''
    };
  },
  mounted() {
    this.loadUserData();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    loadUserData() {
      let user_id = this.$route.params.id
      api.get(`/api/v1/users/${user_id}/`)
        .then(response => {
          this.userData = response.data;
          this.loadPosts(user_id);
          (this.userData.number_of_posts == 1) ? this.postText = "Publicación" : this.postText = "Publicaciones";
        })
    },
    loadPosts(user_id) {
      if (this.nextPage == null)
        return;

      api.post(`/api/v1/posts/get_posts/?page=${this.nextPage}`, { 'user_id': user_id, 'filter_by_user': true })
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
    handleScroll() {
      let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      if (bottomOfWindow && this.hasNext) {
        console.log("bottom scroll");
        this.nextPage++;
        this.loadPosts();
      }
    },
  }
}
</script>
<style>
.post-gallery img {
  width: 100%;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 250px;
  height: 250px;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.7s ease;
}

.image-container:hover .image-overlay {
  opacity: 1;
}

.vertical-center {
  left: 45%;
}
.img-thumbnail :hover {
  background: #0051ff;
  opacity: 0.6;
}

.img-thumbnail {
  width: 250px;
  height: 250px;
  padding: .25rem;
  border: 1px solid #71b8ff;
  border-radius: .25rem;
  max-width: 100%;
  object-fit: cover;
}


@media (max-width: 599px) {
  .img-thumbnail {
    width: 200px;
    height: 200px;
  }
}
</style>
