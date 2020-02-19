<template>
  <div>
    <LandingPage v-if="!isLoggedIn"></LandingPage>
    <Dashboard v-if="isLoggedIn"></Dashboard>
  </div>

  <!-- Want to show landing page if not logged in, else want to show dashboard -->
  <!-- CURRENT OPTIONS: -->
  <!-- 1. Have dashboard and landing page as Vue components and have logic in Home view to then show whichever component -->
  <!-- 2. Have dashboard and landing page  -->
</template>

<script>
import LandingPage from "@/components/LandingPage.vue";
import Dashboard from "@/components/dashboard/Dashboard.vue"

export default {
  name: "Home",
  components: {
    LandingPage,
    Dashboard
  },
  data() {
    return {
      isLoggedIn: false
    };
  },
};
</script>

<style scoped>
</style>
