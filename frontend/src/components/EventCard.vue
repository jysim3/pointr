<template>
  <div>
    <p>{{ eventData.eventName }}</p>
    <p>{{ eventData.societyName }}</p>
    <p>{{ eventData.location }}</p>
    <p>{{ eventData.eventDate }}</p>
  </div>
</template>

<script>
export default {
  name: "DashboardEventCard",
  props: {
    eventData: {
      type: Object,
      required: true
    }
  }
};
</script>

<style>
</style>