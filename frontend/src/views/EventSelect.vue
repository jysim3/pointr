<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h1> Upcoming Events </h1>
      </div>
      <div class="col d-flex flex-column">
        <span> Sort by </span>
        <div class="d-flex align-items-stretch">
          <a 
            :class="{
              'btn': true,
              'btn-primary': sort !== 'new',
              'btn-secondary': sort === 'new'
            }"
            @click="setSort('new')">New</a>
          <a 
            :class="{
              'btn': true,
              'btn-primary': sort !== 'category',
              'btn-secondary': sort === 'category'
            }"
            @click.prevent="setSort('category')">Category</a>
        </div>
      </div>
    </div>
    <div v-if="status === 'success'">
      <div v-if="sort === 'new'">
        <EventList 
          :event-view-title="`Browse Events`"
          :event-data="eventData" 
        >
          <template #action>
            <span/>
          </template>
        </EventList>
      </div>
      <div v-if="sort === 'category'">
        <div v-for="(d, index) in tags" :key="d.id">
          <EventList 
            :event-view-title="`${d} Events`"
            :event-data="eventByTag(index)" 
          >
            <template #action>
              <span/>
            </template>
          </EventList>
        </div>
      </div>
    </div>
    <Loader v-else-if="status === 'loading'" />
  </div>
</template>

<script>
import axios from 'axios'
import EventList from '@/components/EventList.vue'
import Loader from '@/components/Loader.vue'
export default {
  name: "EventSelect",
  props: {
    queryTags: {
      type: Number,
      default: NaN
    }
  },
  components: {
    EventList, Loader
  },
  data() {
    return {
      tags: this.$store.getters.eventTags
        .filter(e => !this.queryTags || e.id === this.queryTags),
      eventData: [],
      status: '',
      sort: 'new',
    }
  },
  mounted() {
    this.status = 'loading'
    axios.get('/api/event/upcoming?',{
      params: {
        number: 100
      }
    })
      .then(v => {
        this.eventData = v.data.data
        this.status = 'success'
      })
      .catch(e => {
        console.log(e) // eslint-disable-line
      })
  },
  methods: {
    eventByTag(tag){ // eslint-disable-line
      return this.eventData.filter(e => e.tags && e.tags.includes(tag))
    },
    setSort(type) {
      if (type === "new") {
        this.sort = "new"
      } else if (type === "category") {
        this.sort = "category"
      }
    }
  }

}
</script>

<style scoped>
</style>