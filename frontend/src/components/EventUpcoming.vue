<template>
  <EventList
    :event-data="eventData"
    list-style="table"
    event-view-title=""
    :loading="eventDataLoading"
  />
</template>

<script>
import axios from 'axios'
import EventList from '@/components/EventList.vue'
export default {
  components: {
    EventList
  },
  props: {
    type: {
      type: String,
      default: 'normal'
    }
  },
  data () {
    return {
      eventData: [],
      eventDataLoading: false
    }
  },
  mounted() {
    this.eventDataLoading = true
    axios.get('/api/event/upcoming?',{
      params: {
        number: this.type === 'large' ? 100 : 5
      }
    })
      .then(v => {
        this.eventData = v.data.data
        this.eventDataLoading = false
      })
      .catch(e => {
        console.log(e) // eslint-disable-line
      })
  }

}
</script>

<style>

</style>