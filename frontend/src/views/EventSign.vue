<template>
  <EventSignEnterAttendance v-if="eid" :eid="eid" />
  <EventSignEnterCode v-else />
</template>

<script>
import EventSignEnterCode from "@/components/EventSignEnterCode.vue";
import EventSignEnterAttendance from "@/components/EventSignEnterAttendance.vue";

export default {
  name: 'EventSign',
  props: {
    eid: {
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