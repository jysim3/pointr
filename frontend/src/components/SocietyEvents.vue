<template>
  <div class="container">
    <EventList
      :event-view-title="'Upcoming Events for ' + socData.name"
      :event-data="upcomingSocietyEvents"
      list-style="table"
      :loading="eventsLoading"
    />
    <EventList
      :event-view-title="'Past Events for ' + socData.name"
      :event-data="pastSocietyEvents"
      list-style="table"
      :loading="eventsLoading"
    />
    <!--- TODO: more features for admins-->
  </div>
</template>

<script>
import EventList from "@/components/EventList.vue";
import axios from 'axios'
export default {
  components: {
    EventList
  },
  props: {
    socID: {
      type: String,
      required: true
    },
    socData: {
      type: Object,
    }
  },

  data() {
    return {
      pastSocietyEvents: [],
      upcomingSocietyEvents: [],
      eventsLoading: true
    }
  },
  mounted() {
    this.eventsLoading = true
    const urls = [
      '/api/society/events/upcoming',
      '/api/society/events/past',
    ]
    Promise.all(urls.map(u => axios.get(u,{
      params: {
        societyID: this.socID
      }
    })))
      .then(([upcomingSocietyEvents, pastSocietyEvents]) => {
        Object.assign(this.pastSocietyEvents,pastSocietyEvents.data.data)
        Object.assign(this.upcomingSocietyEvents,upcomingSocietyEvents.data.data)
        this.eventsLoading = false


      })
  }

}
</script>

<style>

</style>