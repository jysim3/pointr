<template>
  <div id="dashboard-wrapper">
    <div >
      <div id="upcoming-events-filter" >
        <h2>Upcoming events for </h2>
        <select class="input--select select--admin"  v-model="selectedSociety" name="society-select">
          <option value="" >Select a society</option>
          <option
            v-for="(society, index) in allSocieties"
            :key="index"
            :value="society.societyID"
          >{{ society.societyName }}</option>
        </select>
      </div>
      <Loader v-if="!staffEvents" />
      <DashboardEventView v-if="selectedSociety !== ''" eventViewTitle="" :event-data="selectedSocietyEvents" />
    </div>
    <!--- TODO: ignored to have a "finished" product
    <DashboardEventView :event-view-title="upcomingCreatedEvents.title" :event-data="upcomingCreatedEvents.data" />
    <DashboardEventView :event-view-title="pastCreatedEvents.title" :event-data="pastCreatedEvents.data" />
    --->

  </div>
</template>

<script>
//import { mapGetters } from "vuex";
import Loader from '@/components/Loader.vue'
import {fetchAPI} from '@/util'
import { mapGetters } from 'vuex'
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";

export default {
  name: "DashboardAdmin",
  components: {
    DashboardEventView, Loader
  },
  data() {
    return {
      selectedSociety: "",
      selectedRecentEventsSociety: "",
      upcomingCreatedEvents: {
        title: "Upcoming events",
        data: [],
        loading: true
      },
      pastCreatedEvents: {
        title: "Past created events",
        data: []
      },
    };
  },
  created() {
    fetchAPI(`/api/event/getAllEvents`).then(r => {
      this.allEvents = r.data;
    });
  },
  
  computed: {
    ...mapGetters('user', [
      'staffEvents', 'allSocieties'
    ]),

    selectedSocietyEvents() {
      return this.staffEvents[this.selectedSociety]
    },
  },
};
</script>

<style scoped>
.select--admin {
  border: none;

}
#upcoming-events-filter {
  width: 80%;
  margin: auto;
}
</style>