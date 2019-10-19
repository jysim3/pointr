<template>
  <div>
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
</style>