<template>
  <div class="event-view">
    <!-- It is possible that EventCard might be updated without a reload, 
    it's much more likely that the eventViewTitle will not change, just the data being passed to it. -->
    <h3 class="event-view-title" v-once>{{ eventViewTitle }}</h3>
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
  width: 80%;
  margin: 0 auto;
}

.event-view-title {
  margin-top: 4rem;
  max-width: 500px;
  box-shadow: rgba(59, 59, 95, 0.3) 0px 0px 2rem 0px;
  padding: 10px;
  border-radius: 10px;
  margin: 10px;
}
</style>