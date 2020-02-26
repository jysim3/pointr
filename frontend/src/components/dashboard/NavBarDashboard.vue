<template>
  <NavBar :links="links" />
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "NavBarDashboard",
  components: {
    NavBar
  },
  data() {
    return {
      links: [
        {
          to: "/sign",
          text: "Mark attendance"
        },
        {
          to: '/joinsociety',
          text: 'Join a society'
        }
      ]
    };
  }
};
</script>

<style>
</style>