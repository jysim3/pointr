<template>
  <div v-if="attendees.length != 0" id="attendance-container">
    <h2>Attendance</h2>
    <ul>
      <li v-for="(attendee, index) in attendees" :key="index">
        <div id="icons">
            {{ attendee.name }} - {{ attendee.points }}
            <i @click="edit(attendee)" class="material-icons">edit</i>
            <!-- DELETE ICON -->
            <i v-on:click="del(attendee)" class="material-icons">close</i>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
// import { apiURL } from "@/util.js"

export default {
  name: "Attendees",
  props: ["eid", "attendees"],
  mounted() {},
  methods: {
    edit(attendee) {
      const data = {
        zID: attendee.zID,
        eventID: this.eid,
        points: attendee.points - 1 + 2
      }
      fetchAPI('/api/points','POST', data)

    },
    del(attendee) {
      const data = {
        zID: attendee.zID,
        eventID: this.eid
      }
      fetchAPI('/api/points','DELETE', data)

    },
  }
};
</script>

<style>
li {
  list-style-type: none;
  margin-left: -3rem;
  background-color: white;
  color: black;
  border-radius: 0.5rem;
  display: block;
  padding: 1rem;
}

.material-icons {
  cursor: pointer;
}

ul {
  margin-top: 2rem;
}
</style>