<template>
  <div>
    <EventCodeDisplay :eventID="eventID" />
    <h1 id="welcome-header">Welcome to {{ this.name }}</h1>
    <!-- TODO: add more event information here -->
    <h2 id="mark-attendance-header">Sign your attendance</h2>
    <div id="qr-and-form-container">
      <div style="display:flex;flex-direction:column;">
      <EventQRCode :eventID="this.eventID" />
        <button
          class="btn btn-primary"
          @click="downloadCsv"
        >Download csv</button>
      </div>
      <EventAdminAttendance :eventID="this.eventID" />
    </div>
    <div id="event-attendance-container">
      <EventAttendance class="attendee" :eventID="eventID" :attendees="reversedParticipants" />
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
    EventAdminAttendance,
    FormError
  },
  data() {
    return {
      name: "",
      participants: [],
      error: ""
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
      return `${window.location.host}/sign/${this.eventID}`;
    },
    reversedParticipants() {
      const participantsCopy = this.participants.slice();
      return participantsCopy.reverse();
    }
  },
  methods: {
    downloadCsv() {
      fetchAPI(`/api/event/getAttendance?eventID=${this.eventID}`)
      .then(r => {
        var fileURL = window.URL.createObjectURL(new Blob([r.data]));
        var fileLink = document.createElement('a');
        fileLink.href = fileURL;
        fileLink.setAttribute('download', `${this.name}.csv`);
        document.body.appendChild(fileLink);
        fileLink.click();
      })
    },
    async fetchAttendees() {
      try {
        const response = await fetchAPI(`/api/event/?eventID=${this.eventID}`);
        this.participants = response.data.attendance;
        this.name = response.data.eventName;

      } catch (error) {
        console.log(error.response) //eslint-disable-line
      }
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
.btn-primary {
  margin-right: 2rem;
}
</style>