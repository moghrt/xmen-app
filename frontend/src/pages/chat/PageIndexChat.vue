<template>
  <q-page class="constrain-more q-pa-md">
    <div class="q-gutter-y-md" style="max-width: 600px">
      <q-card>
        <q-tabs ref="qtabs" v-model="tab" dense class="text-grey" active-color="primary" indicator-color="primary"
          align="justify" narrow-indicator>
          <q-tab name="direct-messages" label="Mensajes" />
          <q-tab name="groups" label="Grupos" />
        </q-tabs>
        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="groups">
            <q-scroll-area class="vh-65">
              <div v-for="room in groupRooms" :key="room.id">
                <component-user-resume v-if="checkAvailableRooms(room.tags, false)" :toUrl="'/chat/' + room.id"
                  :avatarUrl="room.image" :name="room.name" :caption="room.caption"></component-user-resume>
                <q-separator v-if="checkAvailableRooms(room.tags, false)" class="q-my-md" />
              </div>
            </q-scroll-area>
          </q-tab-panel>
          <q-tab-panel name="direct-messages">
            <q-scroll-area class="vh-65">
              <div v-for="room in messagesRooms" :key="room.id">
                <component-user-resume v-if="checkAvailableRooms(room.name, true)"
                  :toUrl="'/chat/' + room.id" :avatarUrl="room.image" :name="room.name"
                  :caption="room.caption"></component-user-resume>
                <q-separator  v-if="checkAvailableRooms(room.name, true)" class="q-my-md" />
              </div>
            </q-scroll-area>
            <div class="row justify-center">
              <q-btn round color="primary" icon="eva-plus-outline" @click="openModal" />
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
    <component-add-chat-modal :value="showModal" @submit="onAcceptModal" @cancel="onCancelModal" />
  </q-page>
</template>

<script>
import { api } from 'boot/axios'
import { ref } from 'vue';
import { authStore } from 'stores/store';
import ComponentUserResume from 'src/components/ComponentUserResume.vue';
import ComponentAddChatModal from 'src/components/ComponentAddChatModal.vue';
export default {
  name: "PageIndexChat",
  components: {
    ComponentUserResume,
    ComponentAddChatModal
  },
  setup() {
    const store = authStore();
    return {
      tab: ref('direct-messages'),
      store,
    };
  },
  data() {
    return {
      dataComponent: ref({
        to_url: '/chat/general',
        avatar_url: "http://localhost:8000/media/avatars/4.jpg",
        name: "Pruebini",
        caption: "Caption"
      }),
      rooms: [],
      showModal: false,
      modalData: ref([]),
      groupRooms: ref([]),
      messagesRooms: ref([]),
    };
  },
  mounted() {
    this.getRooms();
  },
  methods: {
    getRooms() {
      api.get("/api/v1/rooms/")
        .then(response => {
          this.groupRooms = response.data.filter(room => room.type == 'grupos');
          this.messagesRooms = response.data.filter(room => room.type == 'mensajes');
        })
    },
    checkAvailableRooms(roomArgs, checkByName) {
      let userArgs = (checkByName) ? this.store.user_name : this.store.user_tags;
      let chatRoomList = roomArgs.split(',').map(arg => arg.trim());
      let userList = userArgs.split(',').map(arg => arg.trim());

      // Si el chat no tiene argumentos, es público para todos.
      if (chatRoomList.length == 0)
        return true;

      let coincidences = chatRoomList.filter(arg => userList.includes(arg));

      if (coincidences.length > 0)
        return true;

      return false;
    },
    openModal() {
      this.showModal = true;
      console.log(this.showModal);
    },
    onAcceptModal(usersSelected) {
      console.log(usersSelected);
      // Crear el chat con el uui de los integrantes separados por guiones (-).
      let data = {
        authorId: this.store.user_id,
        authorName: this.store.user_name,
        image: this.store.user_avatar_url,
        items: usersSelected,
      };
      api.post("/api/v1/rooms/create_room/", data)
        .then(response => {
          console.log(response);
          this.getRooms();
        })
      this.showModal = false;
    },
    onCancelModal() {
      this.showModal = false;
    }
  },
}
</script>
<style>
#ig_app {
  padding-top: 85px;
  padding-bottom: 80px;
}

#ig_header {
  position: fixed;
  top: 0;
  padding-top: 15px;
  padding-bottom: 15px;
  color: var(--app-primary-text-color);
  background-color: #fff;
  z-index: 10;
  font-size: 24px;
  font-weight: 700;
  border-bottom: 1px solid rgba(0, 0, 0, .05);
}

#ig_header .col-4 {
  font-size: 28px;
}

#ig_header img {
  width: 20%;
  border-radius: 100%;
  max-height: 50px;
  max-width: 50px;
}

#ig_header span.ig_chat_user {
  display: inline-block;
  position: relative;
  top: -6px;
  width: 75%;
  padding-left: 8px;
}

#ig_header span.ig_chat_chat_last_active {
  position: absolute;
  display: block;
  font-size: 14.5px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.45);
  margin-top: -5px;
}

#ig_header .text-right i {
  color: rgba(0, 0, 0, 0.85);
}

/**/

#ig_chat_box img {
  width: 100%;
  border-radius: 100%;
  max-height: 32px;
  max-width: 32px;
}

.row>.col-12 {
  font-size: 14px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.5);
}

.row .col-2 {
  align-items: flex-end;
  display: flex;
}

#ig_chat_box .row:not(:first-child) {
  margin-top: 30px;
}

.row .msg span {
  display: table;
  background-color: rgba(0, 0, 0, 0.06);
  font-size: 16.5px;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: 30px;
  color: rgba(0, 0, 0, 0.95);
}

.row .m-msg span {
  border-radius: 0 30px 30px 0;
  margin-top: 2.5px;
  text-align: left;
}

.row.r-msg .m-msg span:first-child {
  border-radius: 30px 30px 30px 0;
}

.row.r-msg .m-msg span:last-child {
  border-radius: 0 30px 30px 30px;
}

.row.s-msg .msg span {
  background: linear-gradient(0deg, rgba(64, 95, 222, 1) 0%,
      rgba(117, 48, 203, 1) 100%);
  color: #fff;
  display: table;
}

.row.s-msg .m-msg {
  direction: rtl;
}

.row.s-msg .m-msg span {
  direction: ltr;
  border-radius: 30px 0 0 30px;
}

.row.s-msg .m-msg span:first-child {
  border-radius: 30px 30px 0 30px;
}

.row.s-msg .m-msg span:last-child {
  border-radius: 30px 0 30px 30px;
}

/**/

#ig_chat_footer {
  width: 100%;
  bottom: 0;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 15px;
  padding-left: 15px;
}

#ip_search {
  width: 100%;
  font-size: 18px;
  font-weight: 400;
  padding: 15px 10px 15px 60px;
  border: none;
  box-shadow: inset 0 0 3px rgba(0, 0, 0, 0.07);
  border-radius: 200px;
  background-color: #efefef;
}

#ig_chat_footer .ig_camera {
  position: absolute;
  display: inline-block;
  width: 40px;
  height: 40px;
  background-color: rgba(64, 95, 222, 1);
  text-align: center;
  color: #fff;
  font-size: 19px;
  line-height: 40px;
  border-radius: 100%;
  margin-left: 10px;
  margin-top: 9.5px;
}

#ig_chat_footer ul {
  position: absolute;
  top: 0;
  right: 0;
  margin-top: 10px;
  margin-right: 15px;
}

#ig_chat_footer ul li {
  float: left;
  list-style: none;
  font-size: 25px;
  margin-right: 22px;
  color: rgba(0, 0, 0, 0.95);
}
</style>
