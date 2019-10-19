<template>
  <div v-if="attendees.length != 0" id="attendance-container">
    <h2>Attendance</h2>
    <ul>
      <li v-for="(attendee, index) in attendees" :key="index">
        {{ attendee.name }}
        <!-- EDIT ICON -->
        <i @click="edit" class="material-icons">edit</i>
        <!-- DELETE ICON -->
        <i @click="del(attendee)" class="material-icons">close</i>
      </li>
    </ul>
  </div>
</template>

<script>
import {fetchAPI} from '@/util.js'
// import { apiURL } from "@/util.js"

export default {
  name: "Attendees",
  props: ["eid", "attendees"],
  mounted() {},
  methods: {
    edit() {

    },
    del(attendee) {
      const data = {
        zID: attendee.zID,
        eventID: this.edi
      }
      fetchAPI('/api/points','DELETE', data)

    },
  }

};
</script>

<style>
li {
    list-style-type: none;
}

.material-icons {
    cursor: pointer;
}
</style>