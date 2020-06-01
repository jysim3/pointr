<template>
  <div>
    <div id="app">
      <Loader v-show="isLoading" />
      <div v-show="!isLoading">
      <NavBar />
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Footer from '@/components/Footer'
import NavBar from "@/components/NavBar.vue";
import Loader from "@/components/Loader.vue";
import axios from 'axios'

export default {
  name: "app",
  components: {
    NavBar, Loader,
    Footer
  },
  computed: {
    isLoading () { return this.$store.getters.isLoading},
  },
  created: function() {
    axios.interceptors.response.use(undefined, function (err) {
      return new Promise(function () {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch('logout')
        }
        throw err
      })
    })
  }
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