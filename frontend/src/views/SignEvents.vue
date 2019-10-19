<template>
  <div>
    <h1>Welcome to {{ this.eventName }}!</h1>
    <div class="form-container">
      <form @submit="submitForm">
        <div class="label-input-div">
          <label for>zID</label>
          <input type="text" v-model="zid" />
        </div>
        <div class="label-input-div">
          <label for>Name</label>
          <input type="text" v-model="name" />
        </div>
        <button>Sign attendance</button>
      </form>
    </div>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
export default {
  name: "hi",
  props: {
    eid: String
  },
  mounted() {
    fetchAPI(`/api/event?events=${this.eid}`, "GET").then(j => {
      this.eventName = j.name;
    });
  },
  data() {
    return {
      zid: "",
      name: "",
      eventName: ""
    };
  },
  methods: {
    submitForm(e) {
      const data = {
        zID: this.zid,
        name: this.name,
        eventID: this.eid
      };
      e.preventDefault();
      fetchAPI("/api/attend", "POST", data)
        .then(() => {
          window.location.path = "/u/" + this.zid;
        })
        .catch(e => alert(e));
    }
  }
};
</script>

<style scoped>
  h2 {
    text-align: center;
  }
  .form-container {
    margin-top: 3rem;
  }
</style>