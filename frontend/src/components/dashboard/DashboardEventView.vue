<template>
  <div class="event-view">
      <DashboardEventCard
        v-for="(event, index) in events"
        :key="index"
        :eventData="event"
      ></DashboardEventCard>
  </div>
</template>

<script>
import DashboardEventCard from "@/components/dashboard/DashboardEventCard.vue";

export default {
  name: "DashboardEventView",
  components: {
    DashboardEventCard
  },
  props: {
    events: {
      type: Array,
      required: true
    }
  }
};
</script>

<style>
</style>