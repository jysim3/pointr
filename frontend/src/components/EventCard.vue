<template>
  <div class="event-card">
    <router-link :to="`/${eventData.eventID}`">
      <h3>{{ eventData.eventName }}</h3>
      <p class="event-info">by {{ eventData.societyName }} @ <b>{{ eventData.location }}</b></p>
      <p class="event-info">On {{ eventData.eventDate }}</p>
    </router-link>
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
a {
  font-weight: normal;
}
.event-card {
  border-top: 3px solid var(--c-secondary-dark);
  padding: 1rem;
}

.event-info {
  margin: 1rem 0;
}
</style>