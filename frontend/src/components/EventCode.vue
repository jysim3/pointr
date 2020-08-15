<template>
  <div class="d-flex flex-column text-center ">
    <div class="d-flex flex-column align-content-center flex-grow-1 mb-3">
      <h4>Sign in using QR Code</h4>
      <EventQRCode
        :url="signURL"
      />
    </div>
    <div class="d-flex flex-column align-content-center ">
      <h4>Sign in manually</h4>
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
        <div
          ref="event-code-bar"
          class="event-code-bar"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import EventQRCode from "@/components/event/EventQRCode.vue";
import moment from 'moment'
export default {
  components: {
    EventQRCode,
  },
  props: {
    eventID: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      eventCode: "",
      refreshID: ""
    }
  },
  computed: {
    signURL() {
      return window.location.host + this.$router.resolve({ 
        name: 'event',
        params: {
          eventID: this.eventID,
        },
        query: {
          code: this.eventCode
        }
      }).href
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
  beforeUnmount() {
    clearInterval(this.refreshID)
  },
  methods: {
    getCode() {
      axios.get('/api/event/attend/code', {
        params: { eventID: this.eventID }
      }).then(r => {
        const data = r.data.data
        this.eventCode = data.code
      })
    },
    startRefreshCode() {
      this.$refs['event-code-bar'].style = `animation: decrease ${this.refreshInterval/1000}s ease infinite;`
      this.getCode()
      this.refreshID = setInterval(() => {
        this.getCode()
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