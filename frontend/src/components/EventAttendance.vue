<template>
  <div id="attendance">
    <!-- <h2 id="attendance-header">Attendance<span v-if="!hasAttendees"> ({{ attendees.length }})</span></h2> -->
    <h2 id="attendance-header">Attendance ({{ attendees.length }})</h2>
    <div id="attendees-container" v-if="attendees.length != 0">
      <EventAttendee
        v-for="(attendee, index) in attendees"
        :key="index"
        :eid="eid"
        :attendee="attendee"
      />
    </div>
    <h3 v-else id="no-attendees-msg">All attendees will appear here.</h3>
  </div>
</template>

<script>
import EventAttendee from "@/components/EventAttendee.vue";

export default {
  name: "EventAttendance",
  components: {
    EventAttendee
  },
  props: {
    eid: String,
    attendees: Array
  }
};
</script>

<style scoped>
.attendee:first-of-type {
  border-top-right-radius: var(--border-radius);
  border-top-left-radius: var(--border-radius);
}

.attendee:last-of-type {
  border-bottom-right-radius: var(--border-radius);
  border-bottom-left-radius: var(--border-radius);
}

#attendance {
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#attendance-header {
  text-align: center;
}

#no-attendees-msg {
  text-align: center;
  font-weight: 400;
  margin: 1rem 0;
}

#attendees-container {
  width: 100%;
  margin: 1rem 0 2rem 0;
}
</style>