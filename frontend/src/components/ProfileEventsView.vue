<template>
  <!-- Shows all the events for a given user -->
  <div class="event-view">
    <div v-for="(society, index) in societiesData" :key="index">
      <h1>{{ society.name }}</h1>
      <p v-for="(event, index) in societiesData.events" :key="index">{{ event.name }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileEventsView",
  props: {
    societiesData: Array
  }
};
</script>

<style>
</style>