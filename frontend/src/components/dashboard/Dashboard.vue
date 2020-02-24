<template>
  <div>
    <!-- <router-link tag="button" to="/create" class="btn btn-primary">Create an event</router-link> -->
    <!-- <button @click="joinSociety" class="btn btn-primary">Join a society</button> -->
    <DashboardNavigation />
    <DashboardEventVue :events="upcomingEvents" />
    <DashboardEventVue :events="recentlyAttendedEvents" />
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import DashboardNavigation from "@/components/dashboard/DashboardNavigation.vue";
import DashboardEventVue from "@/components/dashboard/DashboardEventVue.vue";

export default {
  name: "Dashboard",
  components: {
    DashboardNavigation,
    DashboardEventVue
  },
  data() {
    return {
      showJoinSociety: false,
      upcomingEvents: [],
      recentlyAttendedEvents: []
    };
  },
  created() {
    // Decoding token from tokenCheck mixin
    fetchAPI(`/api/user/getAllSocieties?zID=${this.getZID()}`).then(r => {
      // TODO: think about performance, should we be requesting all of the events from server?
      // Now we have a list of events that are upcoming for the user
      // TODO: FORMAT: [{'society': 'UNSW Hall', 'events': [{}]}]
      // TODO: shouldn't this route need a token instead of a zID?

      // Currently this will get the next five upcoming events.
      this.upcomingEvents = r.message.slice(0, 5);
    });

    fetchAPI(`/api/user/`, "GET")
    .then(j => {
      this.recentlyAttendedEvents = j.events.slice(0, 5);
    })
  }
};
</script>

<style>
</style>