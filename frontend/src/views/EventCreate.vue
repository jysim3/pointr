<template>
  <div class="container">
    <Form
      :back-link="eventID ? {name:'event',params: {eventID}} : null"
      @submit="submitEventForm"
    >
      <template #header>
        <h2>{{ eventID ? 'Edit' : 'Create an' }} event</h2>
      </template>

      <InputModule
        v-model="name"
        required
        name="title"
        label="Event title"
        type="input"
      />

      <InputModule
        v-model="location"
        required
        name="location"
        label="Location"
        type="input"
      />

      <InputModule
        v-model="description"
        required
        name="description"
        label="Description"
        type="textarea"
      />

      <InputModule
        v-model="society"
        required
        label="Society"
        type="select"
        :options="availableSocieties"
      />

      <InputModule
        v-model="startDate"
        required
        name="startDate"
        label="Start Date"
        type="date"
        @input="updateDate(startDate)"
      />

      <InputModule
        v-model="startTime"
        required
        name="startTime"
        label="Start Time"
        type="time"
      />

      <InputModule
        v-model="endDate"
        required
        name="startDate"
        label="End Date"
        type="date"
      />

      <InputModule
        v-model="endTime"
        required
        name="endTime"
        label="End Time"
        type="time"
      />

      <InputModule
        v-model="visibility"
        name="visibility"
        required
        label="Visibility (beta, not in used)"
        type="radio"
        :options="visibilityOptions"
      />


      <template #footer>
        <div>
          <button
            v-if="eventID"
            type="button"
            class="btn btn-warning"
            @click="deleteEvent"
            @focusout="deleteConfirmation = 0"
          >
            {{ deleteConfirmation === 0 ? 'Delete Event' : 'Are you sure?' }}
          </button>
          <button
            type="submit"
            class="btn btn-primary"
          >
            {{ eventID ? 'Edit' : 'Create' }} Event
          </button>
        </div>
      </template>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import InputModule from "@/components/input/Input.vue";
import Form from "@/components/Form";

export default {
  name: "EventCreate",
  components: {
    InputModule,
    Form
  },
  props: {
    eventID: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      deleteConfirmation: 0,
      name: "",
      location: "",
      society: "",
      startDate: "",
      endDate: "",
      description: "",
      startTime: "",
      endTime: "",
      visibility: "",
      availableSocieties: this.$store.getters[
        "user/societies"
      ].admins.map(s => ({
        value: s.id,
        label: s.name
      })),
      visibilityOptions: [{
        value: 'public',
        label: 'Public'
      },
      {
        value: 'private',
        label: 'Private'
      }]
    };
  },
  mounted(){
    this.getEventInfo()
  },
  methods: {
    updateDate() {
      if (this.endDate === '' || new Date(this.endDate) < new Date(this.startDate)) {
        this.endDate = this.startDate
      }

    },
    deleteEvent() {
      if (this.deleteConfirmation === 0) {
        this.deleteConfirmation = 1
        return
      }
      axios.delete('/api/event',{
        params: {
          eventID: this.eventID
        }
      }).then(() => {
        this.$router.push('/')
      })
    },
    getEventInfo() {
      if (!this.eventID) {
        return;
      }
      this.$store.commit("loading", true);
      axios.get(`/api/event?eventID=${this.eventID}`)
        .then(response => {
          const data = response.data.data;
          this.name = data.name;
          this.location = data.location;
          this.society = data.society[0].id;
          this.description = data.description;
          this.startTime = data.start.split(' ')[1].split(':').slice(0,2).join(':')
          this.startDate = data.start.substr(0,10)
          this.endTime = data.end.split(' ')[1].split(':').slice(0,2).join(':')
          this.endDate = data.start.substr(0,10)
          // this.visibility = data.visibility
          console.log(data)
          this.isAdmin = this.$store.getters["user/isSocietyAdmin"](
            data.society
          );
        })
        .catch(c => console.log(c))
        .finally(() => this.$store.commit("loading", false));
    },
    submitEventForm() {
      const data = {
        name: this.name,
        start: new Date(this.startDate + " " + this.startTime),
        end: new Date(this.endDate + " " + this.endTime),
        description: this.description,
        location: this.location,
        status: 0,
        // visibility: this.visibility,
        tags: [0],
        hasQR: true,
        hasAccessCode: false,
        hasAdminSignin: true,
        public: this.publicEvent
      };
      axios({
        url: "/api/event",
        data: data,
        params: {
          societyID: this.society,
          eventID: this.eventID
        },
        method: this.eventID ? 'PATCH' : 'POST'
      }).then(response => {
        console.log(response.data.data)
        this.$router.push({
          name: "event",
          params: { eventID: response.data.data.id }
        });
      })
        .catch(error => {
                    console.log(error.response); //eslint-disable-line
        });
    }
  }
};
</script>

<style scoped>
textarea {
    max-width: 20rem;
}
</style>
