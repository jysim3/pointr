<template>
  <div>
    <LandingPage v-if="!userIsAuthenticated"></LandingPage>
    <Dashboard v-else></Dashboard>
  </div>
</template>

<script>
import auth from "@/mixins/auth"
import LandingPage from "@/components/LandingPage.vue";
import Dashboard from "@/components/dashboard/Dashboard.vue";

export default {
  name: "Home",
  mixins: [auth],
  components: {
    LandingPage,
    Dashboard
  }
};
</script>

<style scoped>
</style>
