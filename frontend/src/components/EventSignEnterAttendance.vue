<template>
  <div>
    <div class="form-container">
      <div class="form">
        <h2>Sign attendance</h2>
        <EventCard :eventData="eventData" />
        <button
          v-if="!eventSignSuccess"
          @submit.prevent="submitEventSignAttendance"
          class="btn btn-primary"
        >Sign as {{ userName }} ({{ zID }})</button>
        <div v-else>
          <h3 v-if="eventAlreadySigned">Already signed this event!</h3>
          <h3 v-else>Success!</h3>
          <router-link to="/">Return to home</router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
import EventCard from "@/components/EventCard.vue";

export default {
  name: "EventSignEnterAttendance",
  props: {
    eid: {
      type: String,
      required: true
    }
  },
  components: {
    EventCard
  },
  data() {
    return {
      zID: "",
      userName: "",
      eventData: {},
      eventSignSuccess: false,
      eventAlreadySigned: false
    };
  },
  created() {
    fetchAPI(`/api/event?eventID=${this.eid}`, "GET").then(j => {
      this.eventData = j.msg;
    });

    fetchAPI(`/api/user/info`, "GET").then(j => {
      this.userName = j.msg.name;
      this.zID = j.msg.zID;
      // Checking if this event's ID matches with a user's signed event.
      this.eventAlreadySigned = j.msg.events.some(
        event => event.eventID === this.eventData.eventID
      );
    });
  },
  methods: {
    submitEventSignAttendance() {
      const data = {
        zID: this.zID,
        eventID: this.eid
      };
      fetchAPI("/api/event/attend", "POST", data)
        .then(r => {
          if (r.status === 200) {
            this.eventSignSuccess = true;
          }
        })
        .catch(e => alert(e));
    }
  }
};
</script>

<style scoped>
</style>