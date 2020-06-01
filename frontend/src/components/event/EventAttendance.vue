<template>
    <div id="" class="container attendance-container">
        <!-- <h2 id="attendance-header">Attendance<span v-if="!hasAttendees"> ({{ attendees.length }})</span></h2> -->
        <h2 id="attendance-header">Attendance ({{ attendees.length }})</h2>
        <div class="d-flex attendance-container-data">
          <div class="box">
            <div class="fieldGroup" v-for="(field, index) in allFields" :key="index">
            <input 
              v-model="checkedFields"
              :value="field"
              type="checkbox"
              />
            <label class="label">{{field}}</label>
            </div>
          <button
            class="btn btn-primary"
            @click="downloadCsv"
          >Download csv</button>
          </div>
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
                          @click="deleteAttendee(attendee.zID)"
                          v-if="n === 'Actions'"
                          class="material-icons warning "
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
    </div>
</template>

<script>
import axios from 'axios'
import { saveAs } from 'file-saver'

export default {
  name: "EventAttendance",
  components: {
  },
  computed: {
    attendeesData() {
      return this.attendees.map(a => ({
          "Name": `${a.firstname} ${a.lastname}`,
          "zID": a.zID,
          "Attend time": a.time,
          "isArcMember": a.isArc
        }))
    },
    fields() {
      return this.allFields.filter(e => this.checkedFields.includes(e)).concat(['Actions'])
    }
  },
  data() {
    return {
      allFields: ['Name','zID','Attend time','isArcMember'],
      checkedFields: ['Name','zID','Attend time','isArcMember'],
      attendees: [],
    }
  },
  methods: {
    deleteAttendee(zID) {
      axios.delete('/api/event/attend/admin',{
        params: {
          zID,
          eventID: this.eventID
        }
      })
    },
    downloadCsv() {
      const data = this.attendeesData.map(attendee => {
        return this.allFields.reduce((a, c) => {
          if (this.checkedFields.includes(c)){
            a.push(attendee[c])
          }
          return a
        }, [])
      })
      const csvContent = "data:text/csv;charset=utf-8,"
      + this.allFields.filter(f => this.checkedFields.includes(f)) + "\n"
      + data.join("\n")
      saveAs(encodeURI(csvContent), `${this.eventName}.csv`)


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
          this.attendees = r.data.data
        })
        .catch(() => {})

  },
  props: {
    eventID: {
      required: true,
      type: String,
    },
    eventName: {
      required: true,
      type: String
    }
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

.attendance-container {
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
.attendance-container-data {
  align-items: flex-start;
}
.box {
  padding: 1rem ;
  margin-right: 1rem;
  display: flex;
  justify-content: flex-start;
}
.fieldGroup {
  display: flex;
  flex-wrap: nowrap;
  flex-direction: row;
  align-items: baseline; 

}
.fieldGroup .label {
  padding-left: 1rem;
}
</style>