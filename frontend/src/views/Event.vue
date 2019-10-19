<template>
  <div>
    <div id="eid-container">
      <div id="event-code-title">
        <h2 id="eid-header">Event code</h2>
        <h2 id="eid-code">{{ this.eid }}</h2>
      </div>
    </div>
    <h1 class="welcome-header">Welcome to {{ this.name }}</h1>
    <div id="qr-and-form-container">
      <EventQRCode v-bind:eid="this.eid" />
      <!-- <h3 id="event-url">{{ eventURL }}</h3> -->
      <div id="event-form-container" class="form-container">
        <form @submit="submitForm" class="form" id="create-event-form" action>
          <div class="label-input-div">
            <label for>zID</label>
            <input v-model="zid" type="text" required />
          </div>
          <div class="label-input-div">
            <label for>Name</label>
            <input v-model="uname" type="text" required />
          </div>
          <button>Sign attendance</button>
        </form>
      </div>
    </div>
    <Attendees :attendees="this.participants" />
  </div>
</template>

<script>
import Attendees from "@/components/Attendees.vue";
import EventQRCode from "../components/EventQRCode.vue";
import { fetchAPI } from "@/util.js";

export default {
  name: "Event",
  props: ["eid"],
  components: {
    EventQRCode,
    Attendees
  },
  data() {
    return {
      name: "",
      eventId: "",
      participants: [],
      zid: "",
      uname: ""
    };
  },
  mounted() {
    fetchAPI(`/api/event?eventID=${this.eid}`, "GET")
    .then(j => {
      this.name = j.name;
      this.eventId = j.eventID;
      const names = [];
      if (j.participants !== undefined) {
        j.participants.forEach(user => {
            names.push(user["name"]);
        });
        this.participants = names;
        }
    }).catch(e => {
        console.log(e) // eslint-disable-line
    });
  },
  computed: {
    eventURL() {
      return `${window.location.host}/#/e/${this.eid}`;
    }
  },
  methods: {
    submitForm(e) {
      e.preventDefault();
      const data = {
        zID: this.zid,
        uname: this.uname,
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

<style>
@import "../assets/style.css";

#event-url {
  text-transform: none;
  font-family: monospace;
}

#eid-container {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

#event-code-title {
  background-color: white;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.05);
  display: inline-block;
  text-align: center;
  padding: 1rem 3rem;
}

#event-code-title h2 {
  margin: 0;
}

#eid-header {
  font-size: 1rem;
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

</style>