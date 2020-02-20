<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import tokenCheck from "@/mixins/tokenCheck.js"

export default {
  name: "app",
  mixins: [tokenCheck]
};
</script>

<style>
@import "./assets/style.css";
</style>
