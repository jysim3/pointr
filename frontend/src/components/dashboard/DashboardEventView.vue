<template>
  <div class="event-view">
    <!-- It is possible that EventCard might be updated without a reload, 
    it's much more likely that the eventViewTitle will not change, just the data being passed to it. -->
    <h3 v-once>{{ eventViewTitle }}</h3>
    <EventCard v-for="(event, index) in eventData" :key="index" :eventData="eventData"></EventCard>
  </div>
</template>

<script>
import EventCard from "@/components/EventCard.vue";

export default {
  name: "DashboardEventView",
  components: {
    EventCard
  },
  props: {
    eventViewTitle: {
      type: String,
      required: true
    },
    eventData: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
</style>