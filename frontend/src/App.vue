<template>
  <div id="app">

    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
// TODO: import fetchAPI in App.vue instead?
// import auth from "@/mixins/auth"

export default {
  name: "app",
  // mixins: [auth]
};
</script>

<style>
@import "./assets/style.css";
.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
