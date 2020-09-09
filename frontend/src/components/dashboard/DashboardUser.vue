<template>
  <div>
    <EventEnterCode />
    <div class="container">
      <CardContainer
        :title="upcomingEvents.title"
        :loading="upcomingEvents.isLoading"
      > 
        <Card
          v-for="(event, index) in upcomingEvents.data"
          :key="index"
          :data="event"
        />
        <template #options> 
          <router-link
            :to="{name:'eventSelect'}"
            class="link"
          >
            View more
          </router-link>
        </template>
      </CardContainer>
      <CardContainer
        :title="allEvents.title"
        :loading="allEvents.isLoading"
      > 
        <Card
          v-for="(event, index) in allEvents.data"
          :key="index"
          :data="event"
        />
        <template #options> 
          <router-link
            :to="{name:'eventSelect'}"
            class="link"
          >
            View more
          </router-link>
        </template>
      </CardContainer>
    </div>
  </div>
</template>

<script>
import Card from "@/components/EventCard.vue";
import CardContainer from "@/components/CardContainer.vue";
import EventEnterCode from "@/components/eventSign/EventEnterCode.vue";
import axios from 'axios';
export default {
  name: "DashboardUser",
  components: {
    EventEnterCode,
    Card,
    CardContainer
  },
  data() {
    return {
      upcomingEvents: {
        title: "Upcoming events",
        data: [],
        isLoading: false
      },
      allEvents: {
        title: "Browse events",
        data: [],
        isLoading: true
      }
    };
  },
  mounted() {
    this.upcomingEvents.isLoading = true
    this.allEvents.isLoading = true
    const urls = ['/api/user/events/upcoming', '/api/event/upcoming']
    Promise.all(urls.map(u => axios(u))).
      then(response => {
        const [upcomingEvents, allEvents] = response.map(r => 
          r.data.data.map(v => ({
            title: v.name,
            subtitle: v.society[0] && v.society[0].name,
            tags: [
              v.startTime, v.location === null ? '' : `@ ${v.location}`
            ],
            _link: `/event/${v.id}`
          }))
        )
        this.upcomingEvents.data = upcomingEvents
        this.allEvents.data = allEvents
      }).finally(() => {
        this.upcomingEvents.isLoading = false
        this.allEvents.isLoading = false
      })
  }
};
</script>

<style>
/* hr {
  margin-top: 40px;
  margin: 40px;
  border-top: 3px solid #bbb;
} */
</style>