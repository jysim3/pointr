<template>
  <div id="app">
    <router-view />
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
</style>
