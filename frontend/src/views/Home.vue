<template>
  <div>
    <div v-show="!isLoading">
      <LandingPage v-if="!isAuthenticated" />
      <!-- <DashboardAdmin v-else-if="isAdmin"></DashboardAdmin> -->
      <DashboardUser v-else />
    </div>
    <Loader v-show="isLoading" />
  </div>
</template>

<script>
import LandingPage from "@/components/LandingPage.vue";
import DashboardUser from "@/components/dashboard/DashboardUser.vue";
// import DashboardAdmin from "@/components/dashboard/DashboardAdmin.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "Home",
  components: {
    LandingPage,
    DashboardUser,
    // DashboardAdmin,
    Loader
  },
  computed: {
    isLoading () { return this.$store.getters.isLoading},
    isAuthenticated() { return this.$store.getters.isAuthenticated},
  }
};
</script>

<style scoped>
</style>
