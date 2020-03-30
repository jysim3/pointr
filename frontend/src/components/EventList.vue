<template>
  <div >
    <div v-if="eventData">


      <div class="event-view" v-if="listStyle === 'cards'">

        <div class="event-view-title">
          <h2 class="event-view-title-text" v-once>{{ eventViewTitle }}</h2>
          <a class="event-view-more" @click="viewAllData = !viewAllData"
            >View {{viewAllData ? 'less' : 'more'}}</a>
        </div>
        <div class="event-cards " :class="viewAllData ? 'viewAllCards' : ''">
          <EventCard v-for="(event, index) in showEventData" :key="index" :eventData="event"></EventCard>
        </div>
      </div>
      <div class="event-table" v-else-if="listStyle === 'table'">

        <div class="event-view-title">
          <h2 class="event-view-title-text" v-once>{{ eventViewTitle }}</h2>
        </div>
        <Table :data="formattedEventData" :fields="fields"/>
      </div>

    </div>
    <FormError v-else msg="Seems like there is no events at the moment"/> 
      
  </div>
</template>

<script>
import EventCard from "@/components/EventCard.vue";
import FormError from "@/components/FormError.vue";
import Table from "@/components/Table.vue";

export default {
  name: "DashboardEventView",
  components: {
    EventCard, FormError,  Table
  },
  props: {
    eventViewTitle: {
      type: String,
      required: true
    },
    eventData: {
      type: Array,
    },
    listStyle: {
      type: String,
      default: 'cards'
    }
  },
  data() {
    return ({
      viewAllData: false,
      fields: [
        'Date', 'ID', 'Location', 'Event Name'
      ]
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
    },
    formattedEventData() {
      return this.eventData.map(v => ({
        Date: v.eventDate,
        ID: v.eventID,
        Location: v.location,
        'Event Name': v.name,
        _link: `/event/${v.eventID}`
      }))
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

  margin: 0 1rem ;
  /* box-shadow: inset 0 0 2rem 0 rgba(59,59,95,.3);
  border-radius: 5px; */
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
  margin-bottom: 1rem;
}
.event-view-title-text {
  margin-top: 0;
}
.viewAllCards{

  flex-wrap: wrap;
  overflow-x:inherit;
}
.event-table {
  margin: auto;
  padding-top: 4rem;
}

</style>