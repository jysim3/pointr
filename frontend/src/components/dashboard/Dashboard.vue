<template>
  <div>
    <DashboardNavigation />
    <DashboardEventView :eventViewTitle="upcomingEvents.title" :eventData="upcomingEvents.data" />
    <DashboardEventView :eventViewTitle="attendedEvents.title" :eventData="attendedEvents.data" />
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import auth from "@/mixins/auth";
import DashboardNavigation from "@/components/dashboard/DashboardNavigation.vue";
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";

export default {
  name: "Dashboard",
  mixins: [auth],
  components: {
    DashboardNavigation,
    DashboardEventView
  },
  data() {
    return {
      showJoinSociety: false,
      upcomingEvents: {
        title: 'Upcoming Events',
        data: []
      },
      attendedEvents: {
        title: 'Attended Events',
        data: []
      },
    };
  },
  created() {
    fetchAPI(`/api/user/getAllSocieties?zID=${this.getZID()}`).then(r => {
      this.upcomingEvents = r.msg;
    });

    // TODO: need to pass token somehow
    fetchAPI(`/api/user/info`, "POST").then(j => {
      this.attendedEvents.data = j.msg;
    });
  }
};
</script>

<style>
</style>