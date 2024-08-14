<template>
  <q-page class="constrain-more q-pa-md">
    <div class="camera-frame q-pa-md">
      <video v-show="!isFileImage" ref="video" autoplay playsinline class="full-width" />
      <canvas v-show="isFileImage" ref="canvas" class="full-width" height="240" />
    </div>
    <div class="text-center q-pa-md">
      <div class="row">
        <div class="col-6">
          <q-btn v-if="hasCameraSupport" v-show="!isFileImage" color="grey-10" icon="eva-camera" round size="lg"
            @click="captureImage" />
          <q-btn v-if="hasCameraSupport" v-show="isFileImage" class="q-ml-sm" color="negative"
            icon="eva-trash-2-outline" round size="lg" @click="resetImage" />
        </div>
        <div class="col-6">
          <q-file v-if="hasCameraSupport" rounded standout v-model="imageUpload" @input="captureImageFallback"
            accept="image/*" label="Sube una foto">
            <template v-slot:prepend>
              <q-icon name="eva-attach-outline" />
            </template>
            <template v-if="imageUpload" v-slot:append>
              <q-icon name="cancel" @click="resetImage" class="cursor-pointer" />
            </template>
          </q-file>
        </div>
      </div>
      <q-file v-if="!hasCameraSupport" v-show="!isFileImage" outlined v-model="imageUpload"
        @input="captureImageFallback" clearable accept="image/*" label="Sube una foto">
        <template v-slot:prepend>
          <q-icon name="eva-attach-outline" />
        </template>
      </q-file>
    </div>
    <div class="row justify-center q-pa-md">
      <q-input class="col col-sm-8" v-model="post.title" type="text" label="Ponle un título" />
    </div>
    <div class="row justify-center q-pa-md">
      <q-input class="col col-sm-8" v-model="post.description" type="text" label="Escribe algo" />
    </div>
    <div class="row justify-center q-mt-lg">
      <q-btn unelevated rounded color="primary" label="Subir publicación" @click="submitPost" />
    </div>
  </q-page>
</template>

<script>
import { uid } from 'quasar'
import { api } from 'boot/axios'
import { polyfill } from 'md-gum-polyfill'
export default {
  name: 'PageCamera',
  setup() { },
  data() {
    return {
      post: {
        //id: uid(),
        title: '',
        description: '',
        image: null,
        date: Date.now(),
      },
      status: '',
      isFileImage: false,
      imageUpload: null,
      hasCameraSupport: true,
    };
  },
  mounted() {
    this.initCamera();
  },
  beforeUnmount() {
    if (this.hasCameraSupport) {
      this.disableCamera();
    }
  },
  methods: {
    submitPost() {
      var data = new FormData();
      data.append("title", this.post.title);
      data.append("date", this.post.date);
      if (this.post.description != null)
        data.append("description", this.post.description);
      if (this.post.image != null)
        data.append("image", this.post.image, this.post.image.name);

      var headers = {
        "Content-Type": "multipart/form-data",
      };

      api.post("/api/v1/posts/", data, headers)
        .then(response => {
          console.log(response);
          // Si se ha posteado, volvemos al inicio.
          this.$router.push('/');
        })
        .finally(() => {
          this.cleanPostData();
        })
    },
    initCamera() {
      navigator.getUserMedia = (navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia);

      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.$refs.video.srcObject = stream;
        }).catch(error => {
          // Permiso denegado al usar la cámara.
          this.hasCameraSupport = false;
        });
    },
    captureImage() {
      // Recuerda, una referencia directa a un elemento DOM, con ref="foo" y this.$refs.foo.
      let video = this.$refs.video;
      let canvas = this.$refs.canvas;
      let context = canvas.getContext('2d');                        //https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
      let imageUid = uid();

      canvas.width = video.getBoundingClientRect().width;           //https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect
      canvas.height = video.getBoundingClientRect().height;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);  //https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/drawImage
      let aBlob = this.dataURItoBlob(canvas.toDataURL());                         //https://developer.mozilla.org/es/docs/Web/API/HTMLCanvasElement/toDataURL
      this.post.image = this.blobToFile(aBlob, imageUid + ".jpg");  // Añado al blob lo que le falta pra ser un file wapo wapo.
      this.isFileImage = true;

      // Deshabilitar la cámara después de capturar una imagen.
      this.disableCamera();
    },
    resetImage() {
      console.log("reset");
      this.isFileImage = false;
      this.imageUpload = null;
      this.post.image = null;
      this.initCamera();
    },
    disableCamera() {
      // https://developer.mozilla.org/en-US/docs/Web/API/MediaStream/getVideoTracks
      this.$refs.video.srcObject.getVideoTracks().forEach(track => {
        track.stop();
      });
    },
    captureImageFallback(file) {
      this.post.image = file;
      let canvas = this.$refs.canvas;
      let context = canvas.getContext('2d');
      let imageUid = uid();

      // Pastiche de https://stackoverflow.com/questions/10906734/how-to-upload-image-into-html5-canvas
      var reader = new FileReader();
      reader.onload = event => {
        var img = new Image();
        img.onload = () => {
          canvas.width = img.width;
          canvas.height = img.height;
          context.drawImage(img, 0, 0);
          // Una vez dibujada la imagen, mostramos de nuevo el canvas.
        }
        img.src = event.target.result;
      }
      this.isFileImage = true;
      console.log(this.isFileImage);
      reader.readAsDataURL(file.target.files[0]);                       //https://developer.mozilla.org/es/docs/Web/API/HTMLCanvasElement/toDataURL
      let aBlob = file.target.files[0];               //https://developer.mozilla.org/es/docs/Web/API/HTMLCanvasElement/toDataURL
      this.post.image = this.blobToFile(aBlob, imageUid + ".jpg");
    },
    dataURItoBlob(dataURI) {
      // convert base64 to raw binary data held in a string
      // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
      var byteString = atob(dataURI.split(',')[1]);

      // separate out the mime component
      var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]

      // write the bytes of the string to an ArrayBuffer
      var ab = new ArrayBuffer(byteString.length);

      // create a view into the buffer
      var ia = new Uint8Array(ab);

      // set the bytes of the buffer to the correct values
      for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
      }

      // write the ArrayBuffer to a blob, and you're done
      var blob = new Blob([ab], { type: mimeString });
      return blob;
    },
    blobToFile(aBlob, fileName) {
      //A Blob() is almost a File() - it's just missing the two properties below which we will add
      let newBlob = new Blob([aBlob], { type: aBlob.type });
      newBlob.lastModifiedDate = new Date();
      newBlob.name = fileName;
      return newBlob;
    },
    cleanPostData() {
      this.post.title = '';
      this.post.description = '';
      this.post.image = null;
      this.post.date = '';
    },
  },
}
</script>
<style>
.camera-frame {
  border: 2px solid #212121;
  border-radius: 10px;
}

.q-field--standout.q-field--highlighted .q-field__control {
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14), 0 3px 1px -2px rgba(0, 0, 0, 0.12);
  background: rgba(0, 0, 0, 0.05);
}

.q-field--standout.q-field--highlighted .q-field__native,
.q-field--standout.q-field--highlighted .q-field__prefix,
.q-field--standout.q-field--highlighted .q-field__suffix,
.q-field--standout.q-field--highlighted .q-field__prepend,
.q-field--standout.q-field--highlighted .q-field__append,
.q-field--standout.q-field--highlighted .q-field__input {
  color: #4f4f4f;
}
</style>
