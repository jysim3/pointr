<template>
  <div class="event-view">
    <div v-if="eventData">
      <!-- It is possible that EventCard might be updated without a reload, 
      it's much more likely that the eventViewTitle will not change, just the data being passed to it. -->
      <div class="event-view-title">
        <h2 class="event-view-title-text" v-once>{{ eventViewTitle }}</h2>
        <a class="event-view-more" @click="viewAllData = !viewAllData"
          >View {{viewAllData ? 'less' : 'more'}}</a>
      </div>
      <div class="event-cards " :class="viewAllData ? 'viewAllCards' : ''">
        <EventCard v-for="(event, index) in showEventData" :key="index" :eventData="event"></EventCard>
        
      </div>
    </div>
    <FormError v-else msg="Seems like there is no events at the moment"/> 
      
  </div>
</template>

<script>
import EventCard from "@/components/EventCard.vue";
import FormError from "@/components/FormError.vue";

export default {
  name: "DashboardEventView",
  components: {
    EventCard, FormError
  },
  props: {
    eventViewTitle: {
      type: String,
      required: true
    },
    eventData: {
      type: Array,
    }
  },
  data() {
    return ({
      viewAllData: false
    })
  },
  computed: {
    showEventData() {
      if (!this.eventData) {
        return []
      }
      if (this.viewAllData) {
        return this.eventData
      } else {
        return this.eventData.filter((v,i) => {
          return i < 3
        })
      }
    }
  }
};
</script>

<style scoped>
.event-view {
  width: 80%;
  margin: auto;
  padding-top: 4rem;
}
.event-cards {

  /* box-shadow: inset 0 0 2rem 0 rgba(59,59,95,.3);
  border-radius: 5px; */
  margin: 0 1rem ;
  padding: 1rem 1rem 1.25rem 1rem;
  /* background: #e3f2fd; */
  overflow-x: scroll;
  display: flex;
  flex-wrap: nowrap;
}

.event-view-title{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.event-view-title-text {
  margin-top: 0;
}
.viewAllCards{

  flex-wrap: wrap;
  overflow-x:inherit;
}
</style>