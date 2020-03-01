<template>
  <div>
    <form id="form-container--signevent" class="form-container" @submit.prevent="submitEventSignAttendance">
      <Loader v-if="loading"/>
      <div v-else class="form">
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
          <!-- TODO: need padding/margin on this -->
          <router-link to="/">Go to home</router-link>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
import EventCard from "@/components/EventCard.vue";
import Loader from "@/components/Loader.vue";
import auth from "@/mixins/auth";

export default {
  name: "EventSignEnterAttendance",
  mixins: [auth],
  props: {
    eventID: {
      type: String,
      required: true
    }
  },
  components: {
    EventCard,
    Loader
  },
  data() {
    return {
      loading: true,
      zID: "",
      userName: "",
      eventData: {
        eventID: this.eventID
      },
      eventSignSuccess: false,
      eventAlreadySigned: false
    };
  },
  created() {
    fetchAPI(`/api/event/?eventID=${this.eventID}`, "GET").then(j => {
      this.eventData.eventDate = j.eventDate;
      this.eventData.name = j.eventName;
      this.eventData.location = j.location;
      this.eventData.societyName = j.societyName;
      console.log(j); //eslint-disable-line
      this.loading = false
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
        eventID: this.eventID
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