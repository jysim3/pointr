<template>
  <div id="app">
    <NavBar />
    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
import { mapMutations, mapActions } from "vuex";
import { fetchAPI } from "@/util";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "app",
  components: {
    NavBar
  },
  methods: {
    ...mapActions('user' ,[
      'authenticateUser'
    ]),
    ...mapMutations('user', [
      'setIsLoading'
    ])
  },
  async created() {
    if (this.$store.state.user.authToken) {
      //FIXME: Currently this causes the normal NavBar to load before the checks for token validity are done.
      const response = await fetchAPI("/api/auth/validate", "POST");
      // FIXME: backend returns 'true', this is possibly bad for future.
      if (response.status === 200 && response.data.valid === "true") {
        // Now that we now the token is valid we can authenticate the user and validate them
        this.authenticateUser(this.$store.state.user.authToken)
      }
    } else {
      this.setIsLoading(false)
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