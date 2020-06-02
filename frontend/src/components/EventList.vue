<template>
  <div >
    <div v-if="loading">
      <Loader />     
    </div>
    <div v-else-if="eventData">


      <div class="event-view" v-if="listStyle === 'cards'">

        <div class="event-view-title">
          <h3 class="event-view-title-text" v-once>{{ eventViewTitle }}</h3>
          <a class="event-view-more link" @click="viewAllData = !viewAllData"
            >View {{viewAllData ? 'less' : 'more'}}</a>
        </div>

        <FormError v-if="eventData.length === 0" msg="Seems like there is no events at the moment"/> 
        <div v-else class="event-cards " :class="viewAllData ? 'viewAllCards' : ''">
          <EventCard v-for="(event, index) in formattedCardData" :key="index" :data="event"></EventCard>
        </div>

      </div>
      <div class="event-table" v-else-if="listStyle === 'table'">
        <div v-if="eventViewTitle" class="event-view-title">
          <h3 class="event-view-title-text" v-once>{{ eventViewTitle }}</h3>
        </div>
        <FormError v-if="eventData.length === 0" msg="Seems like there is no events at the moment"/> 
        <Table v-else :data="formattedEventData" :fields="fields"/>
      </div>

    </div>
       
  </div>
</template>

<script>
import EventCard from "@/components/EventCard.vue";
import FormError from "@/components/FormError.vue";
import Table from "@/components/Table.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "EventList",
  components: {
    EventCard, FormError,  Table, Loader
  },
  props: {
    eventViewTitle: {
      type: String,
    },
    eventData: {
      type: Array,
    },
    loading: {
      type: Boolean,
      default: false
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
    formattedCardData() {
      return this.eventData.map(v => ({
        title: v.name,
        subtitle: v.societyName,
        tags: [
          v.startTime, v.location === null ? '' : v.location
        ],
        _link: `/event/${v.id}`
      }))
    },
    formattedEventData() {
      return this.eventData.map(v => ({
        Date: v.startTime,
        ID: v.id,
        Location: v.location === null ? '' : v.location,
        'Event Name': v.name,
        _link: `/event/${v.id}`
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
@media only screen and (max-width: 900px) {
  .event-cards {
    margin: 0;
  }
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
  margin-top: 4rem;
  padding: 0;
}

</style>