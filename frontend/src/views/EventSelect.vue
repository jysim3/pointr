<template>
  <div class="event-select">
    <h1> Upcoming Events </h1>
    <EventUpcoming type="large" />
  </div>
</template>

<script>
import EventUpcoming from '@/components/EventUpcoming'
export default {
  components: {
    EventUpcoming 
  }

}
</script>

<style scoped>
.event-select {
    margin: 3rem 0;
}

</style>