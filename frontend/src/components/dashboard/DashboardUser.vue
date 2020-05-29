<template>
  <div>
    <EventEnterCode />
    <div id="dashboard-wrapper">
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
import Loader from "@/components/Loader.vue";
import DashboardEventView from "@/components/EventList.vue";
import EventEnterCode from "@/components/eventSign/EventEnterCode.vue";
import axios from 'axios';
export default {
  name: "DashboardUser",
  components: {
    DashboardEventView,
    Loader,
    EventEnterCode
  },
  data() {
    return {
      upcomingEvents: {
        title: "Upcoming events",
        data: [],
        isLoading: false
      },
      allEvents: {
        title: "Browse events",
        data: [],
        isLoading: true
      }
    };
  },
  mounted() {
    axios({
      url:'/api/event/getAllEvents'
    }).then(r => {
      this.allEvents.data = r.data
    })
    .finally(() => {
      this.allEvents.isLoading = false

    })
  }
};
</script>

<style>
/* hr {
  margin-top: 40px;
  margin: 40px;
  border-top: 3px solid #bbb;
} */
</style>