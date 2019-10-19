<template>
  <div>
    <h1>Welcome to our event!</h1>
    <form @submit="submitForm">
      <label class="inp">
        <span class="label">zid</span>
        <input type="text" v-model="zid" />
      </label>
      <br>
      <label class="inp">
        <span class="label">Name</span>
        <input type="text" v-model="name" />
        <input type="submit" />
      </label>
    </form>
  </div>
</template>
<script>
import {apiURL} from '@/App.vue'
export default {
  name: "hi",
    props: {
        eventID: String
    },
  data() {
    return {
      zid: "",
      name: ""
    };
  },
  methods: {
    submitForm(e) {
        
      console.log(apiURL+'events');// eslint-disable-line
      e.preventDefault();
      fetch(apiURL + '/events', {
            method: 'POST', // or 'PUT'
            body: JSON.stringify(this.data), // data can be `string` or {object}!
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(r => r.json())
        .then(() => {
            window.location.replace('/attended');
        })
        .catch(e => alert("Backend has errors, please try again\nError: "+e))
        
    }
  }
};
</script>
<style scoped></style>