<template>
  <div>
    <NavBarDashboard />
    <EventSignEnterCode />
    <hr>
    <div class="event-lists">
      <Loader v-if="upcomingEvents.status == 'loading'"/>
      <DashboardEventView v-else :eventViewTitle="upcomingEvents.title" :eventData="upcomingEvents.data" />
      <Loader v-if="allEvents.status == 'loading'"/>
      <DashboardEventView v-else :eventViewTitle="allEvents.title" :eventData="allEvents.data" />
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import auth from "@/mixins/auth";
import Loader from "@/components/Loader.vue";
import NavBarDashboard from "@/components/dashboard/NavBarDashboard.vue";
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";
import EventSignEnterCode from "@/components/EventSignEnterCode.vue"
export default {
  name: "DashboardUser",
  mixins: [auth],
  components: {
    NavBarDashboard,
    DashboardEventView,
    Loader,
    EventSignEnterCode 
  },
  data() {
    return {
      upcomingEvents: {
        title: 'Your Events',
        data: [],
        status: "loading"
      },
      allEvents: {
        title: 'Browse Events',
        data: [],
        status: "loading",
      },
    };
  },
  created() {
    fetchAPI(`/api/event/getAllEvents`).then(r => {
      console.log(r) // eslint-disable-line
      this.upcomingEvents.data = r;
      this.upcomingEvents.status = "loaded";
    });
    fetchAPI('/api/user/getUpcomingEvents').then(r => {
      console.log(r) // eslint-disable-line
      this.allEvents.data = r.message;
      this.allEvents.status = "loaded";
    });

    this.status = "loaded"
  }
};
</script>

<style>
.event-lists {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}
hr {
  margin-top: 40px;
  margin: 40px;
  border-top: 3px solid #bbb;
}
</style>