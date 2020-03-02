<template>
  <div>
    <LandingPage v-if="!userIsAuthenticated"></LandingPage>
    <DashboardAdmin v-else-if="userIsAdmin"></DashboardAdmin>
    <DashboardUser v-else></DashboardUser>
  </div>
</template>

<script>
import LandingPage from "@/components/LandingPage.vue";
import DashboardUser from "@/components/dashboard/DashboardUser.vue";
import DashboardAdmin from "@/components/dashboard/DashboardAdmin.vue";

export default {
  name: "Home",
  components: {
    LandingPage,
    DashboardUser,
    DashboardAdmin
  }
};
</script>

<style scoped>
</style>
