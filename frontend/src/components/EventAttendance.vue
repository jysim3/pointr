<template>
  <div id="attendance">
    <!-- <h2 id="attendance-header">Attendance<span v-if="!hasAttendees"> ({{ attendees.length }})</span></h2> -->
    <h2 id="attendance-header">Attendance ({{ attendees.length }})</h2>
    <div id="attendees-container" v-if="attendees.length != 0">
      <div class="attendee" v-for="(attendee, index) in attendees" :key="index">
        <p class="name">{{ attendee.name }}</p>
        <p class="points">{{ attendee.points }} point<span v-if="attendee.points != 1">s</span></p>
        <div class="icons">
          <i @click="edit(attendee)" class="material-icons">edit</i>
          <i @click="del(attendee)" class="material-icons">close</i>
        </div>
      </div>
    </div>
    <h3 v-else id="no-attendees-msg">All attendees will appear here.</h3>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";

export default {
  name: "EventAttendance",
  props: {
    eid: String,
    attendees: Array
  },
  methods: {
    edit(attendee) {
      const data = {
        zID: attendee.zID,
        eventID: this.eid,
        points: parseInt(attendee.points) + 1
      }
      fetchAPI('/api/points','POST', data)
      // .then(r => r.json())
      // .then(r => {
      //   if (r['status'] == "success") {
      //     attendee.points += 1
      //   }
      // })
    },
    del(attendee) {
      const data = {
        zID: attendee.zID,
        eventID: this.eid
      }
      fetchAPI('/api/points','DELETE', data)
    },
  }
};
</script>

<style scoped>
.attendee {
  background-color: white;
  padding: 1rem 2rem;
}

.attendee:first-of-type {
  border-top-right-radius: var(--border-radius);
  border-top-left-radius: var(--border-radius);
}

.attendee:last-of-type {
  border-bottom-right-radius: var(--border-radius);
  border-bottom-left-radius: var(--border-radius);
}

.material-icons {
  cursor: pointer;
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