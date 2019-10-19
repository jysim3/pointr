<template>
  <div>
    <h2>Welcome to {{ this.name }}</h2>
    <h2>Your event code is {{ this.eid }}</h2>
    <EventQRCode v-bind:eid="this.eid" />
    <div class="form-container">
      <form @submit="submitForm" class="form" id="create-event-form" action>
        <h3>{{ eventURL }}</h3>
        <div class="label-input-div">
          <label for>Enter zID</label>
          <input v-model="zid" type="text" required />
        </div>
        <div class="label-input-div">
          <label for>Name:</label>
          <input v-model="uname" type="text" required />
        </div>
        <button>Submit</button>
      </form>
    </div>
    <Attendees :attendees="this.participants" />
  </div>
</template>

<script>
import Attendees from "@/components/Attendees.vue"
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
      uname: "",
    };
  },
  mounted() {
    fetchAPI(`/api/event?events=${this.eid}`, "GET").then(j => {
        this.name = j.name;
        this.eventId = j.eventID;
        const names = []
        j.participants.forEach(user => {
            names.push(user['name'])
        })
        this.participants = names
    });
  },
  computed: {
    eventURL() {
      return `${window.location.host}/e/${this.eid}`;
    }
  }, 
  methods: {
      submitForm(e) {
            e.preventDefault();
            const data = 
            {
                zID: this.zid,
                uname: this.uname,
                eventID: this.eid
            }
            fetchAPI("/api/attend", "POST", data)
            .then(() => {
                this.zid = ''
                this.uname = ''
            })
            .catch(e => alert(e))

      }
  }
};
</script>

<style>
@import "../assets/style.css";
</style>