<template>
  <div>
    <Logo />
    <EventCodeDisplay :eid="eid" />
    <h1 id="welcome-header">Welcome to {{ this.name }}</h1>
    <h2 id="mark-attendance-header">Mark your attendance</h2>
    <div id="qr-and-form-container">
      <EventQRCode :eid="this.eid" />
      <div id="event-form-container" class="form-container">
        <!-- TODO: Have forms be their own component with slots? -->
        <form id="event-form" class="form" @submit.prevent="submitEventAttendance">
          <div class="label-input-div">
            <label class="label" for>zID</label>
            <input class="input" v-model="zID" type="text" required />
          </div>
          <div class="label-input-div">
            <label class="label" for>Name</label>
            <input class="input" v-model="uname" type="text" required />
          </div>
          <button type="submit" class="btn btn-primary">Sign attendance</button>
        </form>
      </div>
    </div>
    <div id="event-attendance-container">
      <EventAttendance class="attendee" :eid="eid" :attendees="reversedParticipants" />
      <!-- TODO: only show last 10 people who have joined? Click 'view all' to show all participants? -->
    </div>
  </div>
</template>

<script>
import EventAttendance from "@/components/EventAttendance.vue";
import EventQRCode from "@/components/EventQRCode.vue";
import EventCodeDisplay from "@/components/EventCodeDisplay.vue";
import Logo from "@/components/Logo.vue"
import { fetchAPI } from "@/util.js";

export default {
  name: "Event",
  props: {
    eid: String
  },
  components: {
    EventQRCode,
    EventAttendance,
    EventCodeDisplay,
    Logo
  },
  data() {
    return {
      name: "",
      participants: [],
      zID: "",
      uname: ""
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
      return `${window.location.host}/#/e/${this.eid}`;
    },
    reversedParticipants() {
      const participantsCopy = this.participants.slice();
      return participantsCopy.reverse();
    }
  },
  methods: {
    submitEventAttendance() {
      const data = {
        zID: this.zID,
        name: this.uname,
        eventID: this.eid
      };
      fetchAPI("/api/event/attend", "POST", data)
        .then(() => {
          this.zID = "";
          this.uname = "";
        })
        .then(() => this.fetchAttendees())
        .catch(e => alert(e));
    },
    fetchAttendees() {
      fetchAPI(`/api/event/?eventID=${this.eid}`, "GET")
        .then(r => {
          this.participants = r.attendance;
          this.name = r.eventName;
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

#qr-container,
#event-form-container {
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