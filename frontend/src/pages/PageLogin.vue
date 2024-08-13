<template>
  <q-page class="container auth-container constrain q-pa-md">
    <div class=" row">
      <left-auth class="large-screen-only max-h-500"></left-auth>
      <div class="right-col text-center">
        <div class="header">
          <img src="/assets/xtagramLogo.png">

          <p class="header__info">
            Red social para jóvenes superdotados.
          </p>
        </div>

        <img class="max-w-200" src="/assets/xtagramLogo2a.png">

        <div class="alert alert-danger err-msg" role="alert" v-show="this.errMessage">
          {{ this.errMessage }}
        </div>

        <form class="q-mt-md">
          <div>
            <q-input type="email" name="email" id="email" class="form-control" placeholder="Dirección de email"
              v-model="email" />
          </div>
          <div>
            <q-input type="password" name="password" id="password" class="form-control" placeholder="Contraseña"
              v-model="password" />
          </div>
          <div class="q-pa-lg full-width q-mt-md">
            <q-btn color="primary" icon="eva-person-outline" label="Login" type="submit" @click.prevent="login" />
          </div>
        </form>
        <p class="q-mt-md text-caption text-grey-5">
          En memoria de Jack Kirby y Stan Lee
        </p>
      </div>
    </div>
  </q-page>
</template>

<script>
import LeftAuth from 'src/components/LeftAuth.vue';
import { api } from 'boot/axios'
import { authStore } from 'stores/store';
const store = authStore();

export default {
  components: { LeftAuth },
  name: 'PageLogin',
  data: function () {
    return {
      email: '',
      password: '',
      errMessage: '',
    };
  },
  mounted() {
  },
  methods: {
    login() {
      if (!this.email) {
        this.errMessage = "email can't be empty";
        return;
      } else if (!this.password) {
        this.errMessage = "password can't be empty";
        return;
      }

      // Limpiamos cabecera y store.
      //axios.defaults.headers.common['Authorization'] = '';
      //localStorage.removeItem("access");

      let formData = {
        email: this.email,
        password: this.password
      }

      api.post('/api/v1/jwt/create/', formData)
        .then(response => {
          let access = response.data.access;
          let refresh = response.data.refresh;
          let user = response.data.user;
          // token en la store y datos de usuario.
          store.setAccess(access);
          store.setRefresh(refresh);

          // Moverse a la Home.
          this.$router.push('/');
        })
        .catch(error => {
          this.errMessage = error;
        })
    }
  },
};
</script>

<style>
img {
  width: 100%;
}

.auth-container .right-col {
  background-color: #fff;
  border: 1px solid #dbdbdb;
  width: 400px;
  float: right;
  margin: 20px 10px 0px 10px;
  padding: 40px;
}

.header__info {
  font-size: 17px;
  line-height: 25px;
  color: #999;
  margin-bottom: 2rem;
  margin-top: 1rem;
}
</style>
