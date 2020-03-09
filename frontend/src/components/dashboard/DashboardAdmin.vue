<template>
  <div id="dashboard-wrapper">
    <div id="upcoming-events-filter">
      <h2>Upcoming events for </h2>
      <select class="input--select select--admin" v-model="selectedUpcomingEventsSociety" name="society-select">
        <option value="all" >all my societies</option>
        <option
          v-for="(society, index) in availableSocieties"
          :key="index"
          :value="society"
        >{{ society.societyName }}</option>
      </select>
    </div>
    <!--- TODO: ignored to have a "finished" product
    <DashboardEventView :event-view-title="upcomingCreatedEvents.title" :event-data="upcomingCreatedEvents.data" />
    <DashboardEventView :event-view-title="pastCreatedEvents.title" :event-data="pastCreatedEvents.data" />
    --->
    <DashboardEventView eventViewTitle="" :event-data="selectedSocietyEvents" />

  </div>
</template>

<script>
//import { mapGetters } from "vuex";
import {fetchAPI} from '@/util'
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";

export default {
  name: "DashboardAdmin",
  components: {
    DashboardEventView
  },
  data() {
    return {
      allEvents: [],
      selectedUpcomingEventsSociety: "all",
      selectedRecentEventsSociety: "",
      upcomingCreatedEvents: {
        title: "Upcoming created events",
        data: []
      },
      pastCreatedEvents: {
        title: "Past created events",
        data: []
      }
    };
  },
  created() {
    fetchAPI(`/api/event/getAllEvents`).then(r => {
      this.allEvents = r.data;
    });

  },
  computed: {
    // TODO: Move this to store
      selectedSocietyEvents() {
        if (this.selectedUpcomingEventsSociety === "all") {
          return this.allEvents
        }
        return this.allEvents.filter(e => {
          return e.societyID === this.selectedUpcomingEventsSociety.societyID
        })

      },
    availableSocieties() {
      // TODO: rename allSocieties getter to something better
      return this.$store.getters['user/allSocieties'];
      //return this.allSocieties.filter(s => !this.allSocieties.includes(s))
    }
  }
};
</script>

<style scoped>
.select--admin {
  border: none;

}
</style>