<template>
  <div>
    <Logo />
    <div class="form-container">
      <form id="create-event-form" class="form" @submit.prevent="submitEventForm">
        <h2>Create an event</h2>
        <div class="label-input-div">
          <label class="label" for>Event title</label>
          <input class="input" v-model="title" type="text" required />
        </div>
        <div class="label-input-div">
          <label class="label" for>Society</label>
          <input class="input" v-model="society" type="text" required />
        </div>
        <div class="label-input-div">
          <label class="label" for>Set default points</label>
          <input class="input" v-model="point" type="number" min="0" required />
        </div>
        <div class="label-input-div">
          <label class="label" for>Show QR Code/Event link</label>
          <input class="input" type="checkbox" checked />
        </div>
        <button type="submit" class="btn btn-primary">Create Event</button>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import router from "@/router/index.js";
import Logo from "@/components/Logo.vue";

export default {
  name: "CreateEvent",
  components: {
    Logo
  },
  data() {
    return {
      title: "",
      society: "",
      point: 1
    };
  },
  methods: {
    submitEventForm() {
      const data = {
        name: this.title,
        owner: "Ivan",
        defaultPoints: this.point,
        zID: "adsfh",
        location: 'Test location',
        eventDate: "19700201"
      };
      fetchAPI("/api/event", "POST", data).then(j => {
        console.log(j); //eslint-disable-line
        router.push({ name: "event", params: { eid: j.eventID } });
      });
    }
  }
};
</script>

<style scoped>
</style>