<template>
  <q-page class="constrain-more q-pa-md overflow-y-hidden">
    <q-item class="no-padding">
      <q-item-section avatar>
        <q-avatar size="32px">
          <img :src="roomImage">
        </q-avatar>
      </q-item-section>
      <q-item-section>
        <q-item-label class="q-my-sm" v-if="connectionReady">{{ roomName }} <span
            class="q-ml-xs connection_ready "><q-badge rounded color="green" /></span></q-item-label>
        <q-item-label class="q-my-sm" v-else>{{ roomName }} <span class="q-ml-xs connection_ready "><q-badge rounded
              color="red" /></span></q-item-label>
      </q-item-section>
    </q-item>
    <div class="row q-col-gutter-lg">
      <div class="col-12">
        <q-card class="card-post q-mb-sm chat" flat bordered>
          <q-item>
            <q-item-section>
              <q-scroll-area class="vh-55" ref="chatScroll" @scroll="onScroll">
                <template v-for="(grp, index) in groupedUsers" :key="index">
                  <div :class="[grp.user_name === this.store.user_name ? 'row s-msg' : 'row r-msg']">
                    <div class="col-12 pl-0 msg m-msg">
                      <p v-if="grp.user_name != this.store.user_name" class="q-my-sm"> {{ grp.user_name }} </p>
                      <span v-for="(val, index) in grp.messages" :key="index"> {{ val.body }} </span>
                    </div>
                  </div>
                </template>
                <q-page-sticky position="bottom-right" :offset="[15, 15]">
                  <q-btn v-if="showNewMessagesIcon" fab icon="eva-email-outline" color="primary"
                    @click="animateScroll()" />
                </q-page-sticky>
              </q-scroll-area>
            </q-item-section>
          </q-item>
        </q-card>
        <section id="ig_chat_footer" class="justify-content-center align-self-center">
          <div class="row">
            <div class="col-12">
              <span class="ig_camera">
                <q-icon name="send" />
              </span>
              <input v-model="newMessage" @keyup.enter="sendMessage" type="text" id="ip_search"
                placeholder="Mensaje...">
            </div>
          </div>
        </section>
      </div>
    </div>
  </q-page>
</template>

<script>
import { api } from 'boot/axios'
import { authStore } from 'stores/store';
import { ref } from 'vue';
export default {
  name: "PageChat",
  setup() {
    const store = authStore();
    return {
      store,
    };
  },
  data() {
    return {
      isLoading: true,
      messages: ref([]),
      webSocket: null,
      connectionReady: false,
      connectionError: false,
      isNewMessages: false,
      showNewMessagesIcon: false,
      newMessage: "",
      nickname: null,
      roomName: null,
      roomImage: null,
      prevSender: this.store.user_name,
      scrollAreaHeigth: ref(0),
      scrollAreaIncrement: 46,
      scrollAreaPercentageForIconTrigger: 0.96,
      currentScrollPercentage: 1,
    };
  },
  mounted() {
    this.initChat();
    this.getConversations();
  },
  computed: {
    groupedUsers() {
      let grouped = [];
      let currentGroup = null;
      let prevUser = null;

      this.messages.forEach(message => {
        if (prevUser == null) {
          prevUser = message.sent_by;
        }

        if (prevUser === message.sent_by) {
          if (currentGroup == null) {
            currentGroup = { user_name: message.sent_by, messages: [message] };
            grouped.push(currentGroup);
          }
          else {
            currentGroup.messages.push(message);
          }
        }
        else {
          currentGroup = { user_name: message.sent_by, messages: [message] };
          grouped.push(currentGroup);
          prevUser = message.sent_by;
        }
      });

      return grouped;
    }
  },
  methods: {
    initChat() {
      let roomId = (this.$route.params['id'])
      let protocol = 'ws';
      let host = document.location.host.split(':')[0];
      let baseUrl = `${protocol}://${host}:8000/`
      let webSocketUrl = `${baseUrl}ws/chat/${roomId}/`;
      this.webSocket = new WebSocket(webSocketUrl);

      // Usa arrow functions wapas wapas. https://stackoverflow.com/questions/44072078/calling-function-in-onopen-event-of-websocket-in-react-js-component
      this.webSocket.onopen = (event) => { this.onSocketOpen(event); };
      this.webSocket.onmessage = (event) => { this.onSocketMessage(event) };
      this.webSocket.onerror = (event) => { this.onSocketError(event) };
    },
    onSocketOpen(event) {
      console.log("conexión con éxito a la sala");
      this.connectionReady = true;
    },
    onSocketMessage(event) {
      let message = JSON.parse(event.data);
      this.messages.push(message);
      (this.store.user_name == message.sent_by) ? this.isNewMessages = false : this.isNewMessages = true;
      this.scrollAreaHeigth += this.scrollAreaIncrement;
      // Muevo el scolll al final si el mensaje es mio o si estoy ya abajo de la pantallla.
      // En caso contrario no lo muevo y sale el icono de mensajes pendientes.
      if (!this.isNewMessages || this.currentScrollPercentage > this.scrollAreaPercentageForIconTrigger) {
        this.animateScroll();
      }
    },
    onSocketError(event) {
      console.log("Socket Error");
      console.log(event);
      this.connectionError = true;
    },
    sendMessage() {
      if (this.newMessage.trim().length == 0)
        return;

      let data = { type: 'message', sent_by: this.store.user_name, author: this.store.user_name, body: this.newMessage };
      this.webSocket.send(JSON.stringify(data));
      this.newMessage = "";
      this.isNewMessages = true;
      //this.animateScroll();
    },
    getConversations() {
      let roomId = (this.$route.params['id'])
      api.get(`/api/v1/rooms/${roomId}/`)
        .then(response => {
          this.messages = response.data.messages;
          this.roomName = response.data.name;
          this.roomImage = response.data.image;
          this.scrollAreaHeigth += this.scrollAreaIncrement * response.data.messages.length;
          this.animateScroll();
        })
    },
    onScroll(source, position) {
      this.currentScrollPercentage = source.verticalPercentage

      if (this.currentScrollPercentage == 1) {
        this.isNewMessages = false;
      }

      if (this.currentScrollPercentage <= this.scrollAreaPercentageForIconTrigger && this.isNewMessages) {
        // Mostrar el icono de que hay mensajes nuevos si no está mostrado ya
        if (!this.showNewMessagesIcon) {
          this.showNewMessagesIcon = true;
        }
      }
      else {
        this.showNewMessagesIcon = false;
      }
    },
    animateScroll() {
      console.log(this.scrollAreaHeigth);
      console.log(this.$refs.chatScroll.getScrollPercentage());
      const duration = 1; // ms - usa 0 para scoll instanténeo.

      this.$refs.chatScroll.setScrollPosition('vertical', this.scrollAreaHeigth, duration);
      this.showNewMessagesIcon = false;
      this.isNewMessages = false;
    },
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

.row .msg {
  margin-top: 5px;
}

.row .msg span {
  display: table;
  background: linear-gradient(0deg, rgb(252, 197, 0) 0%,
      rgb(253, 243, 150) 100%);
  font-size: 10pt;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: 30px;
  color: #000;
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
  background: linear-gradient(0deg, rgba(3, 31, 243, 1) 0%,
      rgba(136, 140, 255, 1) 100%);
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

.m-msg>p {
  font-size: 8pt;
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
