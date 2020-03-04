<template>
  <div>
    <EventSignEnterCode />
    <div class="event-lists">
      <Loader v-if="upcomingEvents.isLoading" />
      <DashboardEventView
        v-else
        :eventViewTitle="upcomingEvents.title"
        :eventData="upcomingEvents.data"
      />
      <Loader v-if="allEvents.isLoading" />
      <DashboardEventView v-else :eventViewTitle="allEvents.title" :eventData="allEvents.data" />
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import Loader from "@/components/Loader.vue";
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";
import EventSignEnterCode from "@/components/EventSignEnterCode.vue";
export default {
  name: "DashboardUser",
  components: {
    DashboardEventView,
    Loader,
    EventSignEnterCode
  },
  data() {
    return {
      upcomingEvents: {
        title: "Upcoming events",
        data: [],
        isLoading: true
      },
      allEvents: {
        title: "Browse events",
        data: [],
        isLoading: true
      }
    };
  },
  created() {
    fetchAPI(`/api/event/getAllEvents`).then(r => {
      console.log("R IS " + r.status); //eslint-disable-line
      this.upcomingEvents.data = r.data;
      this.upcomingEvents.isLoading = false;
    });
    fetchAPI("/api/user/getUpcomingEvents").then(r => {
      console.log("BROWSE EVENTS R IS "); //eslint-disable-line
      console.log(r.data) //eslint-disable-line
      console.log("Length of browse events " + r.data.length); //eslint-disable-line
      this.allEvents.data = r.data;
      this.allEvents.isLoading = false;
    });
  }
};
</script>

<style>
.event-lists {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}
/* hr {
  margin-top: 40px;
  margin: 40px;
  border-top: 3px solid #bbb;
} */
</style>