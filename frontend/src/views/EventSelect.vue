<template>
  <div class="container">
    <h1> Upcoming Events </h1>
    <div v-for="d in tags" :key="d.id">
      <EventList 
        :event-view-title="`${d.value} Events`"
        :event-data="eventByTag(d.id)" >
        <template #action>
          <span/>
        </template>
      </EventList>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import EventList from '@/components/EventList.vue'
export default {
  props: {
    queryTags: {
      type: Number,
      default: -1
    }
  },
  components: {
    EventList
  },
  data() {
    return {
      tags: this.$store.getters.eventTags.filter(e => this.queryTags === -1 || e.id === this.queryTags),
      eventData: []
    }
  },
  mounted() {
    axios.get('/api/event/upcoming?',{
      params: {
        number: 100
      }
    })
      .then(v => {
        this.eventData = v.data.data
        this.eventData = this.eventData.reduce((tagEvents, e)=> {
          e.tags && e.tags.forEach(tag => {
            tagEvents[tag] = tagEvents[tag] || []
            tagEvents[tag].push(e)
          });
          return tagEvents
        }, {})
        this.$store.commit('loading')
      })
      .catch(e => {
        console.log(e) // eslint-disable-line
      })
  },
  methods: {
    eventByTag(tag){
      return this.eventData[tag]
    }
  }

}
</script>

<style scoped>
</style>