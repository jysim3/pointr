<template>
  <div>
    <form
      id="form-container--signevent"
      class="form-container"
      @submit.prevent="submitEventSignAttendance"
    >
      <Loader v-if="loading" />
      <div v-else class="form">
        <h2>Sign attendance</h2>
        <EventCard :eventData="eventData" />
        <button
          v-if="!eventSignSuccess"
          class="btn btn-primary"
          type="submit"
        >Sign as {{ this.$store.state.user.info.name }} ({{ this.$store.state.user.info.zID }})</button>
        <div id="submit-message" v-else>
          <h3 v-if="eventAlreadySigned">Already signed this event!</h3>
          <h3 v-else>Success!</h3>
          <!-- TODO: need padding/margin on this -->
          <router-link id="link--home" to="/">Go to home</router-link>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
import EventCard from "@/components/EventCard.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "EventSignEnterAttendance",
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
      eventData: {
        eventID: this.eventID
      },
      eventSignSuccess: false,
      eventAlreadySigned: false
    };
  },
  created() {
    fetchAPI(`/api/event/?eventID=${this.eventID}`, "GET").then(j => {
      this.eventData.eventDate = j.data.eventDate;
      this.eventData.name = j.data.eventName;
      this.eventData.location = j.data.location;
      this.eventData.societyName = j.data.societyName;
      this.loading = false;
    });

    /* TODO: deleting this check to make sure it's smoother
    // Checking if this event's ID matches with an event the user is already a part of.
    this.eventAlreadySigned = this.$store.getters['user/allEvents'].some(
      event => event.eventID === this.eventData.eventID
    );
    */
  },
  methods: {
    submitEventSignAttendance() {
      fetchAPI("/api/event/attend", "POST", {
        zID: this.zID,
        eventID: this.eventID
      })
        .then(r => {
          if (r.status === 200) {
            this.eventSignSuccess = true;
          }
        })
        .catch(e => console.log(e)); //eslint-disable-line
    }
  }
};
</script>

<style scoped>
/* TODO: don't want event card to change width on submit */
/* TODO: clean up this CSS */
#form-container--signevent {
  margin-top: 3rem;
}

#form-container--signevent .event-card {
  align-self: stretch;
}

#submit-message {
  margin-top: 1rem;
  text-align: center;
}
</style>