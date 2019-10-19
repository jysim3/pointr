<template>
  <div>
    <h2>Welcome to {{ this.name }}</h2>
    <h2>Your event code is {{ this.eid }}</h2>
    <EventQRCode v-bind:eid="this.eid" />
    <div class="form-container">
      <form class="form" id="create-event-form" action>
        <h3>{{ eventURL }}</h3>
        <div class="label-input-div">
          <label for>Enter zID</label>
          <input type="text" required />
        </div>
        <button>Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import EventQRCode from "../components/EventQRCode.vue";
import { fetchAPI } from "@/util.js"

export default {
  name: "Event",
  props: ["eid"],
  components: {
    EventQRCode
  },
  data() {
        return {
            name: ""
        }
  },
  mounted(){
    fetchAPI(`/api/event?events=${this.eid}`, "GET")
    .then(j => {
        this.name = j.name
        console.log(j) //eslint-disable-line
    })
  },
  computed: {
    eventURL() {
      return `${window.location.host}/e/${this.eid}`;
    }
  }
};
</script>

<style>
@import "../assets/style.css";
</style>