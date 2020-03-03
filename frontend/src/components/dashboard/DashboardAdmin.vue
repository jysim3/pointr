<template>
  <div>
    <DashboardEventView :event-view-title="upcomingCreatedEvents.title" :event-data="upcomingCreatedEvents.data" />
    <DashboardEventView :event-view-title="pastCreatedEvents.title" :event-data="pastCreatedEvents.data" />
  </div>
</template>

<script>
// import { fetchAPI } from "@/util";
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";

export default {
  name: "DashboardAdmin",
  components: {
    DashboardEventView
  },
  data() {
    return {
      upcomingCreatedEvents: {
        title: "Upcoming created events",
        data: []
      },
      pastCreatedEvents: {
        title: "Past created events",
        data: []
      }
    };
  },
  // async created() {
  //   const 
  // }
};
</script>

<style>
</style>