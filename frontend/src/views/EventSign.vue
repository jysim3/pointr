<template>
  <EventSignEnterAttendance v-if="eventID" :eventID="eventID" />
  <EventSignEnterCode v-else />
</template>

<script>
import EventSignEnterCode from "@/components/EventSignEnterCode.vue";
import EventSignEnterAttendance from "@/components/EventSignEnterAttendance.vue";

export default {
  name: 'EventSign',
  props: {
    eventID: {
      type: String
    }
  },
  components: {
    EventSignEnterCode,
    EventSignEnterAttendance
  },
}
</script>

<style>

</style>