<template>
  <div>
    <div id="upcoming-events-filter">
      <h2>Upcoming events for </h2>
      <select class="input--select select--admin" v-model="selectedUpcomingEventsSociety" name="society-select">
        <option value="">all my societies</option>
        <option
          v-for="(society, index) in availableSocieties"
          :key="index"
          :value="society"
        >{{ society.societyName }}</option>
      </select>
    </div>
    <DashboardEventView :event-view-title="upcomingCreatedEvents.title" :event-data="upcomingCreatedEvents.data" />
    <DashboardEventView :event-view-title="pastCreatedEvents.title" :event-data="pastCreatedEvents.data" />
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import DashboardEventView from "@/components/dashboard/DashboardEventView.vue";

export default {
  name: "DashboardAdmin",
  components: {
    DashboardEventView
  },
  data() {
    return {
      selectedUpcomingEventsSociety: "",
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
  computed: {
    // TODO: Move this to store
    ...mapGetters('user', [
      'allSocieties'
    ]),
    availableSocieties() {
      // TODO: rename allSocieties getter to something better
      return this.allSocietiesData.filter(s => !this.allSocieties.includes(s))
    }
  }
};
</script>

<style scoped>
.select--admin {
  border: none;

}
</style>