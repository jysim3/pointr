<template>
  <div>
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
            <input class="input" v-model="zid" type="text" required/>
          </div>
          <div class="label-input-div">
            <label class="label" for>Name</label>
            <input class="input" v-model="uname" type="text" required/>
          </div>
          <button type="submit" class="btn btn-primary">Sign attendance</button>
        </form>
      </div>
    </div>
    <div id="event-attendance-container">
      <EventAttendance :eid="eid" :attendees="participants" />
    </div>
  </div>
</template>

<script>
import EventAttendance from "@/components/EventAttendance.vue";
import EventQRCode from "@/components/EventQRCode.vue";
import EventCodeDisplay from "@/components/EventCodeDisplay.vue"
import { fetchAPI } from "@/util.js";

export default {
  name: "Event",
  props: {
    eid: String
  },
  components: {
    EventQRCode,
    EventAttendance,
    EventCodeDisplay
  },
  data() {
    return {
      name: "",
      // eventId: "",
      participants: [],
      zid: "",
      uname: ""
    };
  },
  mounted() {
    setInterval(() => {
      fetchAPI(`/api/event?eventID=${this.eid}`, "GET")
      .then(j => {
        this.name = j.name;
        // this.eventId = j.eventID;
        this.participants = j.participants;
      }).catch(e => {
          console.log(e) // eslint-disable-line
      });
    }, 1000)
  },
  computed: {
    eventURL() {
      return `${window.location.host}/#/e/${this.eid}`;
    }
  },
  methods: {
    submitEventAttendance() {
      const data = {
        zID: this.zid,
        name: this.uname,
        eventID: this.eid
      };
      fetchAPI("/api/attend", "POST", data)
        .then(() => {
          this.zid = "";
          this.uname = "";
        })
        .catch(e => alert(e));
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

#qr-container, #event-form-container {
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