import { defineStore } from 'pinia'

export const authStore = defineStore('auth', {
  state: () => ({
    access: '',
    refresh: '',
    user_id :'',
    user_name :'',
    user_caption :'',
    user_email :'',
    user_avatar_url :'',
    user_number_of_posts :'',
    user_tags :'',
  }),
  getters: {},
  actions: {
    initializeStore() {
      if (localStorage.getItem("access_token")) {
        this.access = localStorage.getItem("access_token")
        this.refresh = localStorage.getItem("refresh_token")
        this.user_id = localStorage.getItem("user_id")
        this.user_name = localStorage.getItem("user_name")
        this.user_caption = localStorage.getItem("user_caption")
        this.user_email = localStorage.getItem("user_email")
        this.user_avatar_url = localStorage.getItem("user_avatar_url")
        this.user_number_of_posts = localStorage.getItem("user_number_of_post")
        this.user_tags = localStorage.getItem("user_tags")
      }
      else {
        this.access = '';
        this.refresh = '';
        this.user_id = '';
        this.user_name = '';
        this.user_caption = '';
        this.user_email = '';
        this.user_avatar_url = '';
        this.user_number_of_posts = '';
        this.user_tags = '';
      }
    },
    setAccess(access) {
      this.access = access;
      localStorage.setItem("access_token", access);
    },
    setRefresh(refresh) {
      this.refresh = refresh;
      localStorage.setItem("refresh_token", refresh);
    },
    setUser(user) {
      this.user_id = user.id;
      this.user_name = user.name;
      this.user_caption = user.caption;
      this.user_email = user.email;
      this.user_avatar_url = user.avatar_url;
      this.user_number_of_posts = user.number_of_posts;
      this.user_tags = user.tags;
      localStorage.setItem("user_id", user.id);
      localStorage.setItem("user_name", user.name);
      localStorage.setItem("user_caption", user.caption);
      localStorage.setItem("user_email", user.email);
      localStorage.setItem("user_avatar_url", user.avatar_url);
      localStorage.setItem("user_mumber_of_post", user.number_of_posts);
      localStorage.setItem("user_tags", user.tags);
    },
    cleanAccess() {
      this.access = '';
      localStorage.removeItem('access_token');
    },
    cleanRefresh() {
      this.refresh = '';
      localStorage.removeItem('refresh_token');
    },
    cleanUser() {
      this.user_id = '';
      this.user_name = '';
      this.user_caption = '';
      this.user_email = '';
      this.user_avatar_url = '';
      this.user_number_of_posts = '';
      this.user_tags = '';
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_name');
      localStorage.removeItem('user_caption');
      localStorage.removeItem('user_email');
      localStorage.removeItem('user_avatar_url');
      localStorage.removeItem('user_mumber_of_post');
      localStorage.removeItem('user_tags');
    }
  }
})
