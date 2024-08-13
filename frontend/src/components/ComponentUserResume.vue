<template>
  <q-item>
    <q-item-section avatar>
      <a :href="toUrl">
        <q-avatar>
          <img :src="avatarUrl">
        </q-avatar>
      </a>
    </q-item-section>
    <q-item-section>
      <q-item-label>{{ name }}</q-item-label>
      <q-item-label caption>{{ caption }}</q-item-label>
    </q-item-section>
  </q-item>
</template>
<script>
export default {
  name: "ComponentUserResume",
  props: {
    toUrl:{
      type: String,
      default: '',
    },
    avatarUrl:{
      type: String,
      default: '',
    },
    name:{
      type: String,
      default: '',
    },
    caption:{
      type: String,
      default: '',
    },
  },
  setup() {
    return {};
  },
}
</script>
