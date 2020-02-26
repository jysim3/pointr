<template>
  <div class="event-card">
    <h3>{{ eventData.eventName }}</h3>
    <p class="event-info">by {{ eventData.societyName }} @ <b>{{ eventData.location }}</b></p>
    <p class="event-info">On {{ eventData.eventDate }}</p>
  </div>
</template>

<script>
export default {
  name: "EventCard",
  props: {
    eventData: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.event-card {
  border: 3px dashed var(--c-primary);
  padding: 1rem;
}

.event-info {
  margin: 1rem 0;
}
</style>