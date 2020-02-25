<template>
  <div>
      <router-link to="/sign">Mark attendance</router-link>
      <router-link to="/joinsociety">Join a society</router-link>
      <button @click="signOut" class="btn btn-secondary">Sign out</button>
  </div>
</template>

<script>
import { removeToken } from "@/util";

export default {
    name: 'DashboardNavigation',
    methods: {
      signOut() {
        removeToken()
        // TODO: shouldn't need to push a route, should be automatically done by router
      }
    }
}
</script>

<style>

</style>