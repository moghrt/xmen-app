<template>
  <q-dialog v-model="isOpen" persistent @show="load">
    <q-card class="vw-90  q-pa-sm">
      <div class="row q-col-gutter-lg">
        <div class="col-sm-8 col-12">
          <q-input v-model="userSearch" label="Buscar usuario" dense clearable />
        </div>
        <div class="col-sm-8 col-12">
          <q-scroll-area class="vh-45">
            <q-card class="card-post q-mb-xs q-pa-sm" flat bordered v-for="user in filteredItems" :key="user.id">
              <q-item :class="user.selected == 'true' ? 'bg-positive' : '' ">
                <q-item-section avatar>
                  <q-avatar>
                    <img :src="user.avatar_url">
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label>
                    <span class="text-bold">{{ user.name }}</span>
                  </q-item-label>
                  <q-item-label caption>
                    {{ user.caption }}
                  </q-item-label>
                </q-item-section>
                <q-item-section>
                  <div class="q-ml-md">
                    <q-btn round color="primary" :icon="user.selected == 'true' ? 'eva-minus-circle-outline' : 'eva-plus-circle-outline'" @click="addOrRemoveUser(user)" />
                  </div>
                </q-item-section>
              </q-item>
            </q-card>
          </q-scroll-area>
        </div>
      </div>
      <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
        <q-btn fab icon="keyboard_arrow_up" color="primary" />
      </q-page-scroller>
      <q-card-actions align="right">
        <q-btn flat label="Cancelar" color="primary" @click="cancel" />
        <q-btn flat label="Aceptar" color="primary" @click="submit" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from 'vue';
import { api } from 'boot/axios'
import { authStore } from 'stores/store';
export default {
  props: {
    value: {
      type: Boolean,
      required: true,
    },
  },
  setup() {
    const store = authStore();
    return { store };
  },
  data() {
    return {
      isOpen: this.value,
      options: [],
      userSearch: '',
      data: [],
    };
  },
  computed: {
    filteredItems() {
      let query = this.userSearch ? this.userSearch.toLowerCase() : '';
      return this.options.filter(item =>
        item.name.toLowerCase().includes(query)
      );
    },
  },
  watch: {
    value(val) {
      this.isOpen = val;
    },
    isOpen(val) {
      this.$emit('input', val);
    },
  },
  methods: {
    addOrRemoveUser(user){
      let obj = {
        id: user.id,
        name: user.name
      }
      //Comprobar si exixte el usuario.
      if(this.data.some(item => JSON.stringify(item) === JSON.stringify(obj))){
        user.selected = 'false';
        this.data.pop(obj);
      }
      else{
        user.selected = 'true';
        this.data.push(obj);
      }
    },
    load() {
      this.data = [];
      api.post(`/api/v1/users/get_users/`)
        .then(response => {
          this.options = response.data.map(item => ({ ...item, selected: 'false'})).filter(item => item.id != this.store.user_id);  //https://stackoverflow.com/questions/38922998/add-property-to-an-array-of-objects
        })
    },
    submit() {
      this.$emit('submit', this.data);
      this.options = [];
      this.isOpen = false;
    },
    cancel() {
      this.$emit('cancel');
      this.options = [];
      this.isOpen = false;
    },
  },
};
</script>
