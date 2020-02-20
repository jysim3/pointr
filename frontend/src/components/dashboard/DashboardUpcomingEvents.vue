<template>
  <div class="event-view">
      <DashboardEventCard
        v-for="(event, index) in upcomingEvents"
        :key="index"
        :eventData="event"
      ></DashboardEventCard>
  </div>
</template>

<script>
import DashboardEventCard from "@/components/dashboard/DashboardEventCard.vue";

export default {
  name: "UpcomingEvents",
  components: {
    DashboardEventCard
  },
  props: {
    upcomingEvents: Array
  }
};
</script>

<style>
</style>