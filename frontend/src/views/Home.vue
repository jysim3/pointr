<template>
  <div>
    <LandingPage v-if="!isAuthenticatedBool"></LandingPage>
    <Dashboard v-else></Dashboard>
  </div>

  <!-- Want to show landing page if not logged in, else want to show dashboard -->
  <!-- CURRENT OPTIONS: -->
  <!-- 1. Have dashboard and landing page as Vue components and have logic in Home view to then show whichever component -->
  <!-- 2. Have dashboard and landing page  -->
</template>

<script>
import LandingPage from "@/components/LandingPage.vue";
import Dashboard from "@/components/dashboard/Dashboard.vue";
// import { isAuthenticated } from "@/util.js";

export default {
  name: "Home",
  components: {
    LandingPage,
    Dashboard
  },
  computed: {
    isAuthenticatedBool() {
      return false
    }
  }
};
</script>

<style scoped>
</style>
