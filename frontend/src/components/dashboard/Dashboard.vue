<template>
  <div>
    <NavBar :links="links" />
    <DashboardEventView :eventViewTitle="upcomingEvents.title" :eventData="upcomingEvents.data" />
    <DashboardEventView :eventViewTitle="attendedEvents.title" :eventData="attendedEvents.data" />
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import auth from "@/mixins/auth";
import NavBar from "@/components/dashboard/NavBar.vue";
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";

export default {
  name: "Dashboard",
  mixins: [auth],
  components: {
    NavBar,
    DashboardEventView,
  },
  data() {
    return {
      links: [
        {
          to: "/sign",
          text: "Mark attendance"
        },
        {
          to: '/joinsociety',
          text: 'Join a society'
        }
      ],
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