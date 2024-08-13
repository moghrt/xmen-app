<template>
  <q-layout view="lHh Lpr lFf">
    <q-footer class="small-screen-only">
    </q-footer>
    <q-page-container class="bg-grey-1">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: 'MainLayout',
  setup() {

  },
}
</script>
<style>
.q-footer .q-tab__icon {
  font-size: 30px;
}

.q-toolbar__title {
  text-align: left;
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
