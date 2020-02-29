<template>
  <div class="event-view">
    <h2>{{ eventViewTitle }}</h2>
    <EventCard v-for="(event, index) in eventData" :key="index" :eventData="event"></EventCard>
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
.event-view {
  max-width: 500px;
  box-shadow: rgba(59, 59, 95, 0.3) 0px 0px 2rem 0px;
  padding: 10px;
  border-radius: 10px;
  margin: 10px;
}
</style>