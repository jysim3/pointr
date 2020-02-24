<template>
  <div>
      <!-- <router-link to="/"></router-link> -->
      <router-link to="/joinsociety">Join a society</router-link>
      <button @click="signOut" class="btn btn-secondary">Sign out</button>
  </div>
</template>

<script>
export default {
    name: 'DashboardNavigation',
    methods: {
      signOut() {
        localStorage.removeItem('token')
      }
    }
}
</script>

<style>

</style>