<template>
  <div class="box d-flex p-0 py-3 flex-column event-code">
    <h4 class="header">
      Event code
    </h4>
    <h2 class="primary">
      {{ eventID }}
    </h2>
    <h3>
      PIN: {{ eventCode }}
    </h3>
    <div  ref="event-code-bar" class="event-code-bar">
    </div>
      
  </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
export default {
  props: {
    eventID: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      eventCode: ""
    }
  },
  mounted() {
    axios.get('/api/event/attend/code', {
      params: { eventID: this.eventID }
    }).then(r => {
      const data = r.data.data
      this.eventCode = data.code
      this.refreshInterval = data.refreshInterval
      const timeUntilRefresh = moment(data.nextRefresh*1000)-moment()

      setTimeout(() => this.startRefreshCode(), timeUntilRefresh)
    })
  },
  methods: {
    startRefreshCode() {
      this.$refs['event-code-bar'].style = `animation: decrease ${this.refreshInterval/1000}s ease infinite;`
      axios.get('/api/event/attend/code', {
        params: { eventID: this.eventID }
      }).then(r => {
        const data = r.data.data
        this.eventCode = data.code
      })
      setInterval(() => {
        this.$refs['event-code-bar'].style = `animation: decrease ${this.refreshInterval/1000}s ease infinite;`
        axios.get('/api/event/attend/code', {
          params: { eventID: this.eventID }
        }).then(r => {
          const data = r.data.data
          this.eventCode = data.code


        })
      }, this.refreshInterval);
    }
  }

}
</script>

<style>

.event-code-bar {
  
  position: absolute;
  bottom: 0;
  background-color: green;
  height: 5px;
  width: 100%;
  left: 0;
}
@keyframes decrease {
  100% {
    width: 0;
  }
  
}

.event-code {
  position: relative;
  overflow: hidden;
}

</style>