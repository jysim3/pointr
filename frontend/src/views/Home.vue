<template>
  <div>
    <div v-show="!isLoading">
      <LandingPage v-if="!isAuthenticated"></LandingPage>
      <DashboardAdmin v-else-if="isAdmin"></DashboardAdmin>
      <DashboardUser v-else></DashboardUser>
    </div>
    <Loader v-show="isLoading" />
  </div>
</template>

<script>
import { mapState } from "vuex";
import LandingPage from "@/components/LandingPage.vue";
import DashboardUser from "@/components/dashboard/DashboardUser.vue";
import DashboardAdmin from "@/components/dashboard/DashboardAdmin.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "Home",
  components: {
    LandingPage,
    DashboardUser,
    DashboardAdmin,
    Loader
  },
  computed: {
    ...mapState("user", {
      isLoading: state => state.isLoading,
      isAuthenticated: state => state.isAuthenticated,
      isAdmin: state => state.isAdmin
    })
  }
};
</script>

<style scoped>
</style>
