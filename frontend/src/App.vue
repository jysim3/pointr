<template>
  <div id="app">
    <!-- FIXME: NavBar does not update until reload -->
    <NavBar />
    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
import { fetchAPI } from "@/util";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "app",
  components: {
    NavBar
  },
  async created() {
    if (this.$store.user.authToken) {
      const response = await fetchAPI("/api/auth/validate");
      // FIXME: backend returns 'true' don't know if below will ever evaluate.
      if (response.status === 200 && response.data.valid === true) {
        // Now that we now the token is valid we can authenticate the user and validate them
        this.$store.user.dispatch('authenticateUser', this.$store.user.authToken)
      }
    }
  }
};
</script>

<style>
@import "./assets/style.css";
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>