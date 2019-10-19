<template>
  <div id="attendance-container">
    <h2>Attendance</h2>
    <ul>
      <li v-for="(attendee, index) in attendees" :key="index">
        {{ attendee }}
        <!-- EDIT ICON -->
        <i class="material-icons">edit</i>
        <!-- DELETE ICON -->
        <i class="material-icons">close</i>
      </li>
    </ul>
  </div>
</template>

<script>
// import fetchAPI from '@/util.js'
// import { apiURL } from "@/util.js"

export default {
  name: "Attendees",
  props: ["eid", "attendees"],
  mounted() {}
};
</script>

<style>
li {
    list-style-type: none;
}
</style>