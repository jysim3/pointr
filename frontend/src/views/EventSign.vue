<template>
  <EventSignEnterAttendance v-if="eventID" :eventID="eventID" />
  <EventSignEnterCode v-else />
</template>

<script>
import EventSignEnterCode from "@/components/eventSign/EventSignEnterCode.vue";
import EventSignEnterAttendance from "@/components/eventSign/EventSignEnterAttendance.vue";

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