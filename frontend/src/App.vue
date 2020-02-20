<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import auth from "@/mixins/auth.js"

export default {
  name: "app",
  mixins: [auth]
};
</script>

<style>
@import "./assets/style.css";
</style>
