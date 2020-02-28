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
          <label class="label" for>Location</label>
          <input class="input" v-model="location" type="text" required />
        </div>
        <div class="label-input-div">
          <label class="label" for>Society</label>
          <!--
          <input class="input" v-model="society" type="text" required />
          -->
          <select class="input" v-model="society">
            <option v-for="s in userSocieties" :key="s.societyID" :value="s.societyID">{{s.societyName}}</option>
          </select>
        </div>
        <div class="label-input-div">
          <label class="label" for>Date</label>
          <input class="input" v-model="date" type="date" required />
        </div>
        <div class="label-input-div">
          <label class="label" for>Repeat</label>
          <select class="input" v-model="repeat">
            <option value="">No Repeat</option>
            <option value="day">Every Day</option>
            <option value="week">Every Week</option>
            <option value="month">Every Month</option>
          </select>
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
import Logo from "@/components/Logo.vue";

export default {
  name: "EventCreate",
  components: {
    Logo
  },
  data() {
    return {
      title: "",
      location: "",
      society: "",
      date: "",
      endDate: "",
      repeat: "",
      point: 1,
      userSocieties: [
        
      ]
    };
  },
  created() {
      fetchAPI("/api/soc/getAllSocs", "GET").then(j => {
        console.log(j); //eslint-disable-line
        this.userSocieties = j
      });

  },
  methods: {
    submitEventForm() {
      // TODO: clean this up
      const data = {
        zID: "z5000000", 
        name: this.title,
        location: this.location, 
        eventDate: this.date, 
        socID  : this.society
      }
      if (this.repeat !== "") {
          data.endDate= "2020-04-04" ;
          data.recurType= "day";
          data.recurInterval= 6;
          data.isRecur = "True";
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
      fetchAPI("/api/event/", "POST", data).then(j => {
        console.log(j); //eslint-disable-line
        this.$router.push({ name: "event", params: { eventID: j.msg } });
      });
    }
  }
};
</script>

<style scoped>
</style>