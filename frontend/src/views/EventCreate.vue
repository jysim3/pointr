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
        :options="availableSocieties"
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
import axios from 'axios'
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
      description: "",
      startTime: "",
      endTime: "",
      availableSocieties: this.$store.getters['user/societies'].admins.map(s=> ({
        value: s.id, 
        label:s.name
        })),
    };
  },
  methods: {
    async submitEventForm() {
      const data = {
        name: this.title,
        start: new Date(this.date + " " + this.startTime),
        end: new Date(this.date + " " + this.endTime),
        description: this.description,
        location: this.location,
        status: 0,
        tags: [0],
        hasQR: true,
        hasAccessCode: false,
        hasAdminSignin: true,
        public: this.publicEvent
      };
      axios.post('/api/event',data, {
        params: {
          societyID: this.society,
        }
      }).then(response => {
        this.$router.push({ name: "event", params: { eventID: response.data.msg } });
      }) . catch(error => {
        console.log(error.response) //eslint-disable-line
      })
    }
  }
};
</script>

<style scoped>
textarea {
  max-width: 20rem;
}
</style>
