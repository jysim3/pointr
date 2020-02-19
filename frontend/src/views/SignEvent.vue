<template>
  <div>
    <EventCodeDisplay :eid="eid" />
    <h1>Welcome to {{ this.eventName }}!</h1>
    <div id="sign-event-form">
      <form class="form" @submit="submitForm">
        <div class="label-input-div">
          <label class="label" for>zID</label>
          <input class="input" type="text" v-model="zID" />
        </div>
        <div class="label-input-div">
          <label class="label" for>Name</label>
          <input class="input" type="text" v-model="name" />
        </div>
        <button class="btn btn-primary">Sign attendance</button>
      </form>
    </div>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
import router from "@/router/index.js";
import EventCodeDisplay from "@/components/EventCodeDisplay.vue";

export default {
  name: "SignEvent",
  props: {
    eid: String
  },
  components: {
    EventCodeDisplay
  },
  created() {
    fetchAPI(`/api/event?eventID=${this.eid}`, "GET").then(j => {
      this.eventName = j.name;
    });
  },
  data() {
    return {
      zID: "",
      name: "",
      eventName: ""
    };
  },
  methods: {
    submitForm(e) {
      const data = {
        zID: this.zID,
        name: this.name,
        eventID: this.eid
      };
      e.preventDefault();
      fetchAPI("/api/attend", "POST", data)
        .then(() => {
          router.push({ name: "user", params: { zID: this.zID } });
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
#sign-event-form {
  margin-top: 3rem;
}
</style>