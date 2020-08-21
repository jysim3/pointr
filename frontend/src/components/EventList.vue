<template>
  <div>
    <div v-if="loading">
      <Loader />     
    </div>
    <div
      v-else-if="eventData"
      class="container-fluid mt-5"
    >
      <div v-if="listStyle === 'cards'">
        <div class="d-flex justify-content-between py-2">
          <h3
            v-once
          >
            {{ eventViewTitle }}
          </h3>
          <slot name="action">
            <router-link
              :to="{name:'eventSelect'}"
              class="link"
            >
              View more
            </router-link>
          </slot>
        </div>

        <FormError
          v-if="eventData.length === 0"
          msg="Seems like there is no events at the moment"
        /> 
        <div
          v-else
          class="d-flex flex-wrap"
          :class="viewAllData ? 'viewAllCards' : ''"
        >
          <EventCard
            v-for="(event, index) in formattedCardData"
            :key="index"
            :data="event"
          />
        </div>
      </div>
      <div
        v-else-if="listStyle === 'table'"
        class="event-table"
      >
        <div
          v-if="eventViewTitle"
          class="event-view-title"
        >
          <h3
            v-once
            class="event-view-title-text"
          >
            {{ eventViewTitle }}
          </h3>
        </div>
        <FormError
          v-if="eventData.length === 0"
          msg="Seems like there is no events at the moment"
        /> 
        <Table
          v-else
          :data="formattedEventData"
          :fields="fields"
        />
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
      default: '',
      type: String,
    },
    eventData: {
      default: () => [],
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
    formattedCardData() {
      return this.eventData.map(v => ({
        title: v.name,
        subtitle: v.society[0].name,
        tags: [
          v.startTime, 
          v.location === null ? '' : v.location
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