<template>
  <div>
    <div class="form-container">
      <form id="create-event-form" class="form" @submit.prevent="submitEventForm">
        <h2>Create an event</h2>

        <InputModule required 
        label="Event title" 
        type="input" 
        v-model="title" />

        <InputModule required 
        label="Location" 
        type="input" 
        v-model="location" />

        <InputModule required 
        label="Description" 
        type="textarea" 
        v-model="description" />

        <InputModule required 
        label="Society" 
        type="select" 
        :options="availableSocieties.map(s=>({value: s.societyID, label:s.societyName}))"
        v-model="society" />

        <InputModule required 
        label="Date" 
        type="date" 
        v-model="date" />

        <InputModule required 
        label="Start Time" 
        type="time" 
        v-model="startTime" />

        <InputModule required 
        label="End Time" 
        type="time" 
        v-model="endTime" />

        <InputModule 
        label="Repeat" 
        type="select" 
        :options="repeatOptions"
        v-model="repeat" />

        <InputModule required 
        v-if="repeat"
        label="End Date" 
        type="date" 
        v-model="endDate" />

      <InputModule
        label="Public Event?"
        v-model="publicEvent"
        type="checkbox"
        />
        <!-- <label class="label" for>Set default points</label>
        <input class="input" v-model="point" type="number" min="0" required />
        <label class="label" for>Show QR Code/Event link</label>
        <input class="input" type="checkbox" checked /> -->
        <button type="submit" class="btn btn-primary">Create Event</button>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import InputModule from "@/components/input/Input.vue";

export default {
  name: "EventCreate",
  components: {
    InputModule
  },
  data() {
    return {
      title: "",
      location: "",
      society: "",
      date: "",
      endDate: "",
      repeat: "",
      description: "",
      startTime: "",
      endTime: "",
      point: 1,
      publicEvent: "",
      availableSocieties: [],
      repeatOptions: [
        {
          value: "",
          label: "No Repeat"
        },
        {
          value: "day",
          label: "Every day"
        },
        {
          value: "week",
          label: "Every week"
        },
        {
          value: "month",
          label: "Every month"
        },
      ]
    };
  },
  created() {
    this.availableSocieties = this.$store.getters['user/staffSocieties'];
  },
  methods: {
    async submitEventForm() {
      const data = {
        zID: this.$store.state.user.info.zID,
        name: this.title,
        location: this.location,
        eventDate: this.date,
        socID: this.society,
        description: this.description,
        startTime: this.startTime,
        endTime: this.endTime,
        public: this.publicEvent
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
textarea {
  max-width: 20rem;
}
</style>
