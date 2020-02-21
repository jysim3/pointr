<template>
  <div>
    <router-link tag="button" to="/create" class="btn btn-primary">Create an event</router-link>
    <!-- <button @click="joinSociety" class="btn btn-primary">Join a society</button> -->
    <DashboardJoinSociety />
    <DashboardUpcomingEvents :upcomingEvents="upcomingEvents" />
  </div>
</template>

<script>
import jwt from "jsonwebtoken";
import { fetchAPI } from "@/util.js";
import DashboardJoinSociety from "@/components/dashboard/DashboardJoinSociety.vue";
import DashboardUpcomingEvents from "@/components/dashboard/DashboardUpcomingEvents.vue";

export default {
  name: "Dashboard",
  components: {
    DashboardJoinSociety,
    DashboardUpcomingEvents
  },
  data() {
    return {
      showJoinSociety: false,
      upcomingEvents: []
    };
  },
  created() {
    // Decoding token from tokenCheck mixin
    const zID = jwt.decode(this.token);
    fetchAPI(`/api/user/getAllSocieties?zID=${zID}`).then(r => {
      // TODO: think about performance, should we be requesting all of the events from server?
      // Now we have a list of events that are upcoming for the user
      // TODO: FORMAT: [{'society': 'UNSW Hall', 'events': [{}]}]
      // TODO: shouldn't this route need a token instead of a zID?

      // Currently this will get the next five upcoming events.
      this.upcomingEvents = r.message.slice(0, 5);
    });
  }
};
</script>

<style>
</style>