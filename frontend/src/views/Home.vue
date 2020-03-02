<template>
  <div>
    <LandingPage v-if="!isAuthenticated"></LandingPage>
    <DashboardAdmin v-else-if="isAdmin"></DashboardAdmin>
    <DashboardUser v-else></DashboardUser>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import LandingPage from "@/components/LandingPage.vue";
import DashboardUser from "@/components/dashboard/DashboardUser.vue";
import DashboardAdmin from "@/components/dashboard/DashboardAdmin.vue";

export default {
  name: "Home",
  components: {
    LandingPage,
    DashboardUser,
    DashboardAdmin
  },
  computed: {
    ...mapState('user', {
      isAuthenticated: state => state.isAuthenticated,
      isAdmin: state => state.isAdmin
    }),
  }
};
</script>

<style scoped>
</style>
