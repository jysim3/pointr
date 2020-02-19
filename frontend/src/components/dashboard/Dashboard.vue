<template>
  <div>
    <button @click="eventCreate" class="btn btn-primary">Create an event</button>
    <!-- <button @click="joinSociety" class="btn btn-primary">Join a society</button> -->
    <DashboardJoinSociety />
    <DashboardUpcomingEvents :societiesData="userSocieties" />
  </div>
</template>

<script>
import router from "@/router/index.js";
// import { fetchAPI } from "@/util.js";
import tokenCheck from "@/mixins/tokenCheck.js"
import DashboardJoinSociety from "@/components/dashboard/DashboardJoinSociety.vue";
import DashboardUpcomingEvents from "@/components/dashboard/DashboardUpcomingEvents.vue";

export default {
  name: "Dashboard",
  mixins: [tokenCheck],
  components: {
    DashboardJoinSociety,
    DashboardUpcomingEvents
  },
  data() {
    return {
      showJoinSociety: false,
      userSocieties: []
    };
  },
  created() {
    // Want to get all the events for a particular user -> get all the societies user is part of -> get all the events for each of those societies
    // get all the socities for user, then /api/soc/eventsHosted for each society
    // TODO: make this way cleaner
    

    // backend will implement route to get events that are close in the future, can have a 'view all' for a particular society which will get all of them
    // fetchAPI("").then(r => {
    //   r.forEach(society => {
    //      fetchAPI(
    //       `/api/soc/eventsHosted?societyID=${society.societyID}`
    //     ).then(events => {
    //       society['events'] = events
    //       this.usersSocieties.push(society);
    //     });
    //   });
    // });
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