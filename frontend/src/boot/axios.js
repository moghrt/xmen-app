import { boot } from "quasar/wrappers";
import axios from "axios";
import { authStore } from 'src/stores/store';
import Router  from 'src/router/index.js'


// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
// let baseUrl = `${document.location.protocol}//${document.location.host.split(":")[0]}:8080/api/`;

//http://127.0.0.1:8000/api/v1/jwt/create/
//let baseUrl = process.env.VUE_APP_BASE_URL;

let store = authStore();
let protocol = document.location.protocol
let host = document.location.host.split(':')[0];
let baseUrl = `${protocol}//${host}:8000/`
let api = axios.create({ baseURL: baseUrl });

if (process.env.VUE_APP_USE_PYTHONANYWHERE == 'true') {
  baseUrl = process.env.VUE_APP_BACKEND_URL;
}

// Request interceptor
api.interceptors.request.use(async config => {
  let access = store.access;
  if (access) {
    config.headers.Authorization = 'JWT ' + access;
  }
  else {
    config.headers.Authorization = ''
  }
  return config;
},
  error => {
    Promise.reject(error)
  });


// Response interceptor
api.interceptors.response.use((response) => {
  // Handle the response here
  return response
}, (error) => {
  // Handle errors here
  console.log(error);
  // Token expirado.
  if (error.response.status === 401) {
    //Router.push('/login');
    //window.location.href = '/login'
    store.cleanAccess();
    store.cleanUser();
  }
  return Promise.reject(error)
})


export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api, axios };
