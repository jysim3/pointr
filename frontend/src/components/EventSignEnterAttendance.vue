<template>
  <div>
    <form id="form-container--signevent" class="form-container" @submit.prevent="submitEventSignAttendance">
      <div class="form">
        <h2>Sign attendance</h2>
        <EventCard :eventData="eventData" />
        <button
          v-if="!eventSignSuccess"
          class="btn btn-primary"
          type="submit"
        >Sign as {{ userName }} ({{ zID }})</button>
        <div id="submit-message" v-else>
          <h3 v-if="eventAlreadySigned">Already signed this event!</h3>
          <h3 v-else>Success!</h3>
          <router-link to="/">Go to home</router-link>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
import EventCard from "@/components/EventCard.vue";
import auth from "@/mixins/auth";

export default {
  name: "EventSignEnterAttendance",
  mixins: [auth],
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
    fetchAPI(`/api/event/?eventID=${this.eid}`, "GET").then(j => {
      this.eventData = j;
      console.log(j); //eslint-disable-line
    });

    fetchAPI(`/api/user/info`, "POST").then(j => {
      console.log(j); //eslint-disable-line
      this.userName = j.msg.name;
      this.zID = this.getZID();
      // Checking if this event's ID matches with a user's signed event.
      this.eventAlreadySigned = j.msg.events.some(
        event => event.eventID === this.eventData.eventID
      );
    });
  },
  methods: {
    submitEventSignAttendance() {
      fetchAPI("/api/event/attend", "POST", {
        zID: this.zID,
        eventID: this.eid
      })
        .then((this.eventSignSuccess = true)) //TODO: backend currently does not check if user has already signed?
        .catch(e => console.log(e)); //eslint-disable-line
    }
  }
};
</script>

<style scoped>
/* TODO: don't want event card to change width on submit */
#form-container--signevent {
  margin-top: 3rem;
}

#submit-message {
  margin-top: 1rem;
  text-align: center;
}
</style>