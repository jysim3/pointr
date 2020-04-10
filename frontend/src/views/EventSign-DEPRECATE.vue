<template>
  <EventSign v-if="eventID" :eventID="eventID" />
  <EventEnterCode v-else />
</template>

<script>
import EventEnterCode from "@/components/eventSign/EventEnterCode.vue";
import EventSign from "@/components/eventSign/EventSign.vue";

export default {
  name: 'EventSign',
  props: {
    eventID: {
      type: String
    }
  },
  components: {
    EventEnterCode,
    EventSign
  },
}
</script>

<style>

</style>