<template>
  <div class="attendee">
    <h3 class="name">{{ attendee.userName }}</h3>
    <p class="points">{{ pointsString }}</p>
    <div v-if="beingEdited">
      <!-- TODO: proper styling, implement input--number class in style.css -->
      <input type="number" class="input input--number" v-model="newPoints" />
      <i @click="changeBeingEdited" class="material-icons">close</i>
      <i @click="edit" class="material-icons">check</i>
    </div>
    <div class="icons">
      <i @click="changeBeingEdited" class="material-icons">edit</i>
      <i @click="del" class="material-icons">delete</i>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";

export default {
  name: "EventAttendee",
  props: {
    attendee: Object,
    eventID: String
  },
  data() {
    return {
      beingEdited: false,
      newPoints: this.attendee.points
    };
  },
  computed: {
    pointsString() {
      if (this.attendee.points != 1) {
        return `${this.attendee.points} points`;
      } else {
        return `${this.attendee.points} point`;
      }
    }
  },
  methods: {
    changeBeingEdited() {
      this.beingEdited = !this.beingEdited;
    },
    edit() {
      const data = {
        zID: this.attendee.zID,
        eventID: this.eventID,
        points: parseInt(this.newPoints)
      };
      fetchAPI("/api/user/points", "POST", data);
      this.changeBeingEdited();
      // TODO: error handling, improve delay by sending another request after edited?
    },
    del() {
      const data = {
        zID: this.attendee.zID,
        eventID: this.eventID
      };
      fetchAPI(`/api/event/attend?zID=${this.attendee.zID}&eventID=${this.eventID}`, "DELETE", data);
    }
  }
};
</script>

<style scoped>
.attendee {
  background-color: white;
  padding: 1rem 2rem;
}

.material-icons {
  cursor: pointer;
}
</style>