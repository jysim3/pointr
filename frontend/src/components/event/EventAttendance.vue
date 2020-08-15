<template>
  <div
    class="container-fluid "
  >
    <div class="row">
      <!-- <h2 id="attendance-header">Attendance<span v-if="!hasAttendees"> ({{ attendees.length }})</span></h2> -->
      <div class="col">
        <h2 id="attendance-header">
          Attendance ({{ attendees.length }})
        </h2>
      </div>
    </div>
    <div class="row">
      <div class="col-md-3 col-12">
        <div class="box d-flex flex-column align-items-center">
          <div>
            <div
              v-for="(field, index) in allFields"
              :key="index"
              class="d-flex flex-nowrap"
            >
              <input 
                v-model="checkedFields"
                :value="field"
                type="checkbox"
              >
              <label class="pl-1 label">{{ field }}</label>
            </div>
          </div>
          <button
            class="btn btn-primary"
            @click="downloadCsv"
          >
            Download csv
          </button>
        </div>
      </div>
      <div class="col-9">
        <canvas
          ref="graph"
          width="400"
          height="400"
        />
        <table v-if="attendees.length != 0">
          <tr>
            <th />
            <th
              v-for="(n, i) in fields"
              :key="i"
            >
              {{ n }}
            </th>
          </tr>
          <tr
            v-for="(attendee, index) in attendeesData"
            :key="index"
          >
            <!-- class="link" -->
            <td />
            <td
              v-for="(n, i) in fields"
              :key="i"
            >
              <a
                v-if="n === 'Actions'"
                class="material-icons warning "
                @click="deleteAttendee(attendee.zID)"
              >delete</a>
              <i
                v-else-if="n === 'isArcMember'"
                class="material-icons"
              >{{ attendee[n] ? 'check' : 'close' }}</i>
              <span v-else>{{ attendee[n] }}</span>
            </td>
          </tr>
        </table>
        <h3
          v-else
          id="no-attendees-msg"
        >
          All attendees will appear here.
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { saveAs } from 'file-saver'
import Chart from 'chart.js'
import moment from 'moment'

export default {
  name: "EventAttendance",
  components: {
  },
  props: {
    eventID: {
      required: true,
      type: String,
    },
    eventName: {
      required: true,
      type: String
    },
    eventEnd: {
    },
    eventStart: {
    },
  },
  data() {
    return {
      allFields: ['Name','zID','Attend time','isArcMember'],
      checkedFields: ['Name','zID','Attend time','isArcMember'],
      attendees: [],
      chart: null    }
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

  mounted() {
    this.refreshAttendees()
    this.chart = new Chart(this.$refs['graph'], { // eslint-disable-line
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: '# of sign ins',
          data: [],
          borderColor: 'rgba(255, 99, 132, 1)',
          fill: false,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          xAxes: [{
            ticks: {
              autoSkip:false
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    })
    // setInterval(() => {
    //   this.refreshAttendees()
      
    // }, 5000);
  },
  methods: {
    deleteAttendee(zID) {
      axios.delete('/api/event/attend/admin',{
        params: {
          zID,
          eventID: this.eventID
        }
      }).then(() => {
        this.attendees = this.attendees.filter(a => a.zID !== zID)
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
    },
    updateGraph() {
      const round = (m, interval) => {
        return m.minute(Math.floor(m.minute() / interval)*interval) .second(0)
      }
      let start = moment(this.eventStart) 
      let end = moment(this.eventEnd) 
      let interval = 60
      const eventDuration = end.diff(start,"hours")
      if (eventDuration <= 1) {
        interval = 5
      } else if (eventDuration < 2){
        interval = 10
      } else if (eventDuration < 8){
        interval = 30
      }

      start = round(start, interval)
      end = round(end,interval)
      const times = this.attendees.map(a => moment(a.time)).sort().map(a => round(a,interval))
      const data = times.reduce((a, curr) => {
        if (curr in a) {
          a[curr] += 1
        } else {
          a[curr] = 1
        }
        return a
      }, {})
      let labels =[]
      const graphData = []
      for (let i = start; i <= end; i=i.add(interval, "m")){
        labels.push(i.format("LT"))
        if (i in data) {
          graphData.push(data[i])
        }else{
          graphData.push(0)
        }


      }
      this.chart.data.labels=  labels
      this.chart.data.datasets[0].data = Object.values(graphData)
      this.chart.update()

    },
    refreshAttendees() {
      axios.get(`/api/event/attend`,{
        params: {
          eventID: this.eventID
        }
      })
        .then(r => {
          this.attendees = r.data.data
          this.$nextTick(() => this.updateGraph())
        })
        .catch(() => {})

    }
    
  }
};
</script>
