<template>
  <div>
    <div class="form-container">
      <form id="create-event-form" class="form" @submit.prevent="submitEventForm">
        <h2>Create an event</h2>
        <label class="label" for>Event title</label>
        <input class="input" v-model="title" type="text" required />
        <label class="label" for>Location</label>
        <input class="input" v-model="location" type="text" required />
        <label class="label" for>Society</label>
        <select class="input" v-model="society">
          <option
            v-for="s in availableSocieties"
            :key="s.societyID"
            :value="s.societyID"
          >{{s.societyName}}</option>
        </select>
        <label class="label" for>Date</label>
        <input class="input" v-model="date" type="date" required />
        <label class="label" for>Repeat</label>
        <select class="input" v-model="repeat">
          <option value>No Repeat</option>
          <option value="day">Every Day</option>
          <option value="week">Every Week</option>
          <option value="month">Every Month</option>
        </select>
        
        <label class="label" v-if="repeat" for>End Date</label>
        <input class="input" v-if="repeat" v-model="endDate" type="date" required />
        <label class="label" for>Set default points</label>
        <input class="input" v-model="point" type="number" min="0" required />
        <label class="label" for>Show QR Code/Event link</label>
        <input class="input" type="checkbox" checked />
        <button type="submit" class="btn btn-primary">Create Event</button>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";

export default {
  name: "EventCreate",
  data() {
    return {
      title: "",
      location: "",
      society: "",
      date: "",
      endDate: "",
      repeat: "",
      point: 1,
      availableSocieties: []
    };
  },
  created() {
    this.availableSocieties = this.$store.getters['user/staffSocieties'];
  },
  methods: {
    async submitEventForm() {
      // TODO: clean this up
      const data = {
        zID: this.$store.state.user.info.zID,
        name: this.title,
        location: this.location,
        eventDate: this.date,
        socID: this.society
      };
      if (this.repeat !== "") {
        data.endDate = this.endDate;
        data.recurType = this.repeat;
        data.recurInterval = 6;
        data.isRecur = 1;
      } else {
        data.isRecur = 0;
      }

      //  const data = {
      //  zID: "z5111111",
      //  name: "Coffee Night",
      //  location: "CSESoc",
      //  eventDate: "2020-01-01",
      //  endDate: "2020-04-04",
      //  recurType: "day",
      //  recurInterval: 6,
      //  "socID": "8EF48",
      //  "isRecur": "True"
      //  }

      try {
        const response = await fetchAPI("/api/event/", "POST", data);
        this.$router.push({ name: "event", params: { eventID: response.data.msg } });
      } catch (error) {
        console.log(error.response) //eslint-disable-line
      }
    }
  }
};
</script>

<style scoped>
</style>
