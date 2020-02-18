<template>
  <!-- Be able go to create an event -->
  <!-- Be able to join society -->
  <!-- View current events -->
  <!-- View events user went to -->
  <div>
    <button @click="eventCreate" class="btn btn-primary">Create an event</button>
    <!-- <button @click="joinSociety" class="btn btn-primary">Join a society</button> -->
    <JoinSociety />
  </div>
</template>

<script>
import router from "@/router/index.js";
import { fetchAPI } from "@/util.js";
import JoinSociety from "@/components/JoinSociety.vue";

export default {
  name: "Profile",
  data() {
    return {
      showJoinSociety: false,
      usersSocities: []
    };
  },
  created() {
    // get all the socities for user, then /api/soc/eventsHosted for each society
    // TODO: make this way cleaner
    fetchAPI("").then(r => {
      r.forEach(society => {
         fetchAPI(
          `/api/soc/eventsHosted?societyID=${society.societyID}`
        ).then(events => {
          society['events'] = events
          this.usersSocieties.push(society);
        });
      });
    });
  },
  methods: {
    eventCreate() {
      // TODO: this is a common method - repetitive code
      router.push({ name: "create" });
    }
    // joinSociety() {
    //   this.showJoinSociety = true
    // }
  }
};
</script>

<style>
</style>