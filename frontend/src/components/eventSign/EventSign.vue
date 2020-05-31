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
        <EventCard size="lrg" :data="cardData" />
        <button
          v-if="!eventSignSuccess"
          class="btn btn-primary"
          type="submit"
        >Sign as {{ this.$store.state.user.name }} ({{ this.$store.state.user.zID }})</button>
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
import axios from 'axios'
import EventCard from "@/components/EventCard.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "EventSignEnterAttendance",
  props: {
    eventID: {
      type: String,
      required: true
    },
    eventData: {
      type: Object,
      required: true
    }
  },
  components: {
    EventCard,
    Loader
  },
  data() {
    return {
      loading: false,
      eventSignSuccess: false,
      eventAlreadySigned: false
    };
  },
  computed: {
    cardData() {
      return {
        title: this.eventData.name,
        subtitle: this.eventData.description,
        tags: [
          this.eventData.start, this.eventData.location
        ],
        _link: `/event/${this.eventData.eventID}`
      }
    }
  },
  methods: {
    submitEventSignAttendance() {
      axios({
        url: "/api/event/attend", 
        method: "POST", 
        params: {
          eventID: this.eventID
        }
      }).then(() => {
          this.eventSignSuccess = true;
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