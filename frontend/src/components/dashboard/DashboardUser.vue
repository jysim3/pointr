<template>
  <div>
    <EventSignEnterCode />
    <hr>
    <div class="event-lists">
      <Loader v-if="upcomingEvents.isLoading"/>
      <DashboardEventView v-else :eventViewTitle="upcomingEvents.title" :eventData="upcomingEvents.data" />
      <Loader v-if="allEvents.isLoading"/>
      <DashboardEventView v-else :eventViewTitle="allEvents.title" :eventData="allEvents.data" />
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import auth from "@/mixins/auth";
import Loader from "@/components/Loader.vue";
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";
import EventSignEnterCode from "@/components/EventSignEnterCode.vue"
export default {
  name: "DashboardUser",
  mixins: [auth],
  components: {
    DashboardEventView,
    Loader,
    EventSignEnterCode 
  },
  data() {
    return {
      upcomingEvents: {
        title: 'Your Events',
        data: [],
        isLoading: true
      },
      allEvents: {
        title: 'Browse Events',
        data: [],
        isLoading: true
      },
    };
  },
  created() {
    fetchAPI(`/api/event/getAllEvents`).then(r => {
      console.log(r) // eslint-disable-line
      this.upcomingEvents.data = r;
      this.upcomingEvents.isLoading = false;
    });
    fetchAPI('/api/user/getUpcomingEvents').then(r => {
      console.log(r) // eslint-disable-line
      this.allEvents.data = r.message;
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
hr {
  margin-top: 40px;
  margin: 40px;
  border-top: 3px solid #bbb;
}
</style>