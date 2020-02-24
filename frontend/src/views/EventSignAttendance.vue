<template>
  <div>
    <h2>Welcome to {{ eventName }}!</h2>
    <h3>EVENT DETAILS HERE</h3>
    <button
      @submit.prevent="submitEventSignAttendance"
      class="btn btn-primary"
    >Sign as {{ userName }} ({{ zID }})</button>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";

export default {
  name: "SignEvent",
  props: {
    eid: {
      type: String,
      required: true
    }
  },
  created() {
    fetchAPI(`/api/event?eventID=${this.eid}`, "GET").then(j => {
      this.eventName = j.name;
    });

    fetchAPI(`/api/user`, "GET")
    .then(j => {
      this.userName = j.firstName + j.lastName
    })
  },
  data() {
    return {
      zID: "",
      userName: "",
      eventName: ""
    };
  },
  methods: {
    submitEventSignAttendance() {
      const data = {
        zID: this.zID,
        eventID: this.eid
      };
      fetchAPI("/api/event/attend", "POST", data)
        // .then(() => {
        //   this.$route.push({ name: "user", params: { zID: this.zID } });
        // })
        .catch(e => alert(e));
    }
  }
};
</script>

<style scoped>
</style>