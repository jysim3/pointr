<template>
    <div id="attendance" class="container">
        <!-- <h2 id="attendance-header">Attendance<span v-if="!hasAttendees"> ({{ attendees.length }})</span></h2> -->
        <h2 id="attendance-header">Attendance ({{ attendees.length }})</h2>
        <table v-if="attendees.length != 0">
            <tr>
                <th></th>
                <th v-for="(n, i) in fields" :key="i">{{n}}</th>
            </tr>
            <tr v-for="(attendee, index) in attendeesData" :key="index">
                <!-- class="link" -->
                <td></td>
                <td v-for="(n, i) in fields" :key="i">
                    <a
                        @click="deleteAttendee()"
                        v-if="n === 'Actions'"
                        class="material-icons warning"
                    >delete</a>
                    <i
                        v-else-if="n === 'isArcMember'"
                        class="material-icons"
                    >{{ attendee[n] ? 'check' : 'close'}}</i>
                    <span v-else>{{ attendee[n] }}</span>
                </td>
            </tr>
        </table>
        <h3 v-else id="no-attendees-msg">All attendees will appear here.</h3>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "EventAttendance",
  components: {
  },
  computed: {
    attendeesData() {
      return this.attendees.map(a => ({
          "Name": a.userName,
          "zID": a.attendanceTime,
          "isArcMember": a.isArcMember
        }))
    }
  },
  data() {
    return {
      fields: ['Name','zID','isArcMember','Actions'],
      attendees: [],
    }
  },
  methods: {
    deleteAttendee() {
      // const data = {
      //   zID: this.attendee.zID,
      //   eventID: this.eventID
      // };
      // axios.post(`/api/event/attend?zID=${this.attendee.zID}&eventID=${this.eventID}`);
    }
  },

  mounted() {
        axios.get(`/api/event/attend`,{
            params: {
                eventID: this.eventID
            }
        })
        .then(r => {
          console.log(r.data)
          this.attendees = r.data.attendance
        })
        .catch(() => {})

  },
  props: {
    eventID: String,
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
    font-size: 1rem;
}

#attendance-header {
    text-align: center;
}

#no-attendees-msg {
    text-align: center;
    font-weight: 400;
    margin: 1rem 0;
}
</style>