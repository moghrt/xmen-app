<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar class="constrain">
        <q-btn class="large-screen-only q-mr-sm " color="grey-1" icon="eva-camera-outline" flat round size="18px"
          to="/camera" />
        <q-separator class="large-screen-only" vertical spaced color="grey-1" />
        <q-toolbar-title class="text-grand-hotel text-h4">
          Xtagram
        </q-toolbar-title>
        <q-btn class="large-screen-only" color="grey-1" icon="eva-home-outline" flat round size="18px" to="/" />
        <q-btn color="grey-1" icon="eva-message-square-outline" flat round size="18px" to="/chat/" />
        <q-btn class="small-screen-only" color="grey-1" icon="eva-person-outline" flat round size="18px">
          <q-menu>
            <q-list>
              <q-item clickable v-close-popup :to="`/profile/${store.user_id}`">
                <q-item-section>Ver perfil</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="logout">
                <q-item-section>Cerrar sesión</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>
    <q-footer class="small-screen-only">
      <q-tabs classs="tex-grey-10" active-bg-color="warning" active-color="dark" indicator-color="transparent">
        <q-route-tab to="/" icon="eva-home-outline" />
        <q-route-tab to="/camera" icon="eva-camera-outline" />
        <q-route-tab to="/user-list" icon="eva-people-outline" />
      </q-tabs>
    </q-footer>
    <q-page-container class="bg-grey-1">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { authStore } from 'stores/store';
import { api } from 'boot/axios'
import { useRouter } from 'vue-router'
export default {
  name: 'MainLayout',
  setup() {
    const store = authStore();
    return {
      store
    };
  },
  data() {
    return {};
  },
  beforeCreate() {
    // La Pinia no es una base de datos!. Se va al traste con cada refresh. Con esto recojo del local storage lo que quiero y se lo pongo de vuelta.
    this.store.initializeStore();
  },
  created() {
    this.getMe();
  },
  mounted() {
  },
  methods: {
    getMe() {
      api.get("/api/v1/user/")
        .then(response => {
          let user = response.data;
          this.store.setUser(user);
        })
    },
    getAccessByRefreshToken() {
      api.get("/api/v1/jwt/refresh/")
        .then(response => {
          let access = response.data.access;
          let refresh = response.data.refresh;

          // token en la store.
          this.store.setAccess(access);
          this.store.setRefresh(refresh);
        })
    },
    logout() {
      // Limpio token de acceso y mando al login.
      this.store.cleanAccess();
      this.$router.push('/login');
    }
  }
}
</script>
<style>
.q-footer .q-tab__icon {
  font-size: 30px;
}

.q-toolbar__title {
  text-align: left;
  height: 45px;
}

.q-toolbar {
  padding: 5px 12px;
}

.q-toolbar__title .ellipsis {
  overflow: auto;
}

@media (max-width: 599px) {
  .q-toolbar__title {
    text-align: center;
    margin-left: 50px;
  }
}

@media (min-width: 600px) {
  .q-toolbar__title {
    text-align: center;
  }

  .q-toolbar {
    height: 70px;
  }
}
</style>
