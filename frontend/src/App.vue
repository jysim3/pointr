<template>
  <div>
    <div id="app">
      <Loader v-show="isLoading" />
      <div v-show="!isLoading">
        <NavBar
          v-show="navBar"
          class="mb-5"
        />
        <transition
          name="fade"
          mode="out-in"
        >
          <router-view />
        </transition>
      </div>
    </div>
    <Footer v-show="navBar" />
  </div>
</template>

<script>
import Footer from '@/components/Footer'
import NavBar from "@/components/NavBar.vue";
import Loader from "@/components/Loader.vue";

export default {
  name: "App",
  components: {
    NavBar, Loader,
    Footer
  },
  computed: {
    isLoading () { return this.$store.getters.isLoading},
    navBar () { return this.$store.getters.navBar},
  },
};
</script>

<style>
@import "./assets/style.css";
#app {
  min-height: calc(100vh - 50px);
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>