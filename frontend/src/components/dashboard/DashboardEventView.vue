<template>
  <div class="event-view">
    <h3>{{ eventViewTitle }}</h3>
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