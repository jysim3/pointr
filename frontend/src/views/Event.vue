<template>
  <div>
    <EventCodeDisplay :eventID="eventID" />
    <h1 id="welcome-header">Welcome to {{ this.name }}</h1>
    <!-- TODO: add more event information here -->
    <h2 id="mark-attendance-header">Sign your attendance</h2>
    <div id="qr-and-form-container">
      <EventQRCode :eventID="this.eventID" />
      <EventAdminAttendance :eventID="this.eventID" />
    </div>
    <div id="event-attendance-container">
      <EventAttendance class="attendee" :eventID="eventID" :attendees="reversedParticipants" />
      <!-- TODO: only show last 10 people who have joined? Click 'view all' to show all participants? -->
    </div>
  </div>
</template>

<script>
import EventAttendance from "@/components/EventAttendance.vue";
import EventQRCode from "@/components/EventQRCode.vue";
import EventCodeDisplay from "@/components/EventCodeDisplay.vue";
import EventAdminAttendance from "@/components/EventAdminAttendance.vue";
import { fetchAPI } from "@/util.js";

export default {
  name: "Event",
  props: {
    eventID: String
  },
  components: {
    EventQRCode,
    EventAttendance,
    EventCodeDisplay,
    EventAdminAttendance
  },
  data() {
    return {
      name: "",
      participants: [],
    };
  },
  created() {

    this.fetchAttendees();
    setInterval(() => {
      this.fetchAttendees();
    }, 2000);
  },
  computed: {
    eventURL() {
      return `${window.location.host}/#/e/${this.eventID}`;
    },
    reversedParticipants() {
      const participantsCopy = this.participants.slice();
      return participantsCopy.reverse();
    }
  },
  methods: {
    fetchAttendees() {
      fetchAPI(`/api/event/?eventID=${this.eventID}`)
        .then(r => {
          this.participants = r.data.attendance;
          this.name = r.data.eventName;
          console.log(r) // eslint-disable-line
        })
        .catch(e => {
          console.log(e); // eslint-disable-line
        });
    }
  }
};
</script>

<style scoped>
/* TODO: refactor this CSS */
#welcome-header {
  margin: 2rem 0;
}

#mark-attendance-header {
  text-align: center;
  margin: 3rem 0 2rem 0;
  font-weight: 400;
}

#event-url {
  text-transform: none;
  font-family: monospace;
}

#event-form {
  box-shadow: none;
}

#qr-container {
  display: inline-block;
}

#qr-and-form-container {
  display: flex;
  justify-content: center;
}

#qr-container {
  margin-right: 2rem;
}

#event-attendance-container {
  margin-top: 3rem;
  display: flex;
  justify-content: center;
  font-size: 1.5rem;
}
</style>