<template>
  <div>
    <button @click="eventCreate" class="btn btn-primary">Create an event</button>
    <!-- <button @click="joinSociety" class="btn btn-primary">Join a society</button> -->
    <DashboardJoinSociety />
    <DashboardUpcomingEvents :upcomingEvents="upcomingEvents" />
  </div>
</template>

<script>
import router from "@/router/index.js";
import jwt from "jsonwebtoken";
import { fetchAPI, getToken } from "@/util.js";
import tokenCheck from "@/mixins/tokenCheck.js";
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
      upcomingEvents: []
    };
  },
  created() {
    const zID = jwt.decode(getToken())
    fetchAPI(`api/user/getAllSocieties?zID=${zID}`).then(r => {
      // TODO: think about performance, should we be requesting all of the events from server?
      // Now we have a list of events that are upcoming for the user
      // TODO: FORMAT: [{'society': 'UNSW Hall', 'events': [{}]}]

      // Currently this will get the next five upcoming events.
      this.upcomingEvents = r.message.slice(0, 5);
    });
  },
  methods: {
    eventCreate() {
      // TODO: this is a common method - repetitive code
      router.push({ name: "create" });
    }
  }
};
</script>

<style>
</style>