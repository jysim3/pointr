<template>
  <div id="event-host-view-wrapper">
        <EventCodeDisplay :eventID="eventID" />
        <h1 id="welcome-header">Welcome to {{ this.eventData.name }}</h1>
        <p class="description">{{ this.eventData.description }}</p>
        <!-- TODO: add more event information here -->
        <h2 id="mark-attendance-header">Sign your attendance</h2>
    <div id="qr-and-form-container">
      <div style="display:flex;flex-direction:column;">
      <EventQRCode :eventID="this.eventID" />
      </div>
      <EventAdminAttendance :eventID="this.eventID" />
    </div>
    <div id="event-attendance-container">
      <EventAttendance :eventName="this.eventData.name" class="attendee" :eventID="eventID" />
      <FormError v-show="error" :msg="error" />
      <!-- TODO: only show last 10 people who have joined? Click 'view all' to show all participants? -->
    </div>
  </div>
</template>

<script>
import EventAttendance from "@/components/event/EventAttendance.vue";
import EventQRCode from "@/components/event/EventQRCode.vue";
import EventCodeDisplay from "@/components/event/EventCodeDisplay.vue";
import EventAdminAttendance from "@/components/event/EventAdminAttendance.vue";
import FormError from "@/components/FormError.vue";

export default {
  name: "EventHost",
  props: {
    eventID: String,
    eventData: Object
  },
  components: {
    EventQRCode,
    EventAttendance,
    EventCodeDisplay,
    EventAdminAttendance,
    FormError
  },
  data() {
    return {
      error: ""
    }
  },
  created() {
  },
  computed: {
    eventURL() {
      return `${window.location.host}/event/${this.eventID}`;
    },
    reversedParticipants() {
      const participantsCopy = this.participants.slice();
      return participantsCopy.reverse();
    }
  },
};
</script>

<style scoped>
/* TODO: refactor this CSS */
#event-host-view-wrapper {
  display: flex;
  flex-direction: column;
  align-content: center;
}
#welcome-header {
  margin: 2rem 0;
}
.description {
  text-align: center;
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
.btn-primary {
  margin-right: 2rem;
}
</style>
