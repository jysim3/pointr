<template>
  <div id="dashboard-wrapper">
    <div >
      <div id="upcoming-events-filter" >
        <h2>Upcoming events for </h2>
        <select class="input--select select--admin"  v-model="selectedSociety" name="society-select">
          <option value="all" >All</option>
          <option
            v-for="(society, index) in joinedSocieties"
            :key="index"
            :value="society.societyID"
          >{{ society.societyName }}</option>
        </select>
      </div>
      <Loader v-if="!allEvents" />
      <DashboardEventView v-if="selectedSociety !== ''" eventViewTitle="" :event-data="selectedSocietyEvents" />
    </div>

  </div>
</template>

<script>
//import { mapGetters } from "vuex";
import Loader from '@/components/Loader.vue'
import { mapGetters } from 'vuex'
import DashboardEventView from "@/components/EventList.vue";

export default {
  name: "DashboardAdmin",
  components: {
    DashboardEventView, Loader
  },
  data() {
    return {
      selectedSociety: "all",
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
  },
  
  computed: {
    ...mapGetters('user', [
      'joinedSocieties', 'allSocietyEvents', 'allEvents'
    ]),

    selectedSocietyEvents() {
      if (this.selectedSociety === "all"){
        return this.allEvents
      }
      return this.allSocietyEvents(this.selectedSociety)
    },
  },
};
</script>

<style scoped>
h2 {
  display: inline-block;
  margin-right: 1rem;
}
.select--admin {
  border: none;

}
#upcoming-events-filter {
  width: 80%;
  margin: auto;
}
</style>