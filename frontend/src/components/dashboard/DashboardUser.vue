<template>
  <div>
    <EventSignEnterCode />
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
import EventSignEnterCode from "@/components/eventSign/EventSignEnterCode.vue";
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
};
</script>

<style>
/* hr {
  margin-top: 40px;
  margin: 40px;
  border-top: 3px solid #bbb;
} */
</style>