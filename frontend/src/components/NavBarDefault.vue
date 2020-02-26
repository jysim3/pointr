<template>
  <NavBar :links="links" />
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "NavBarDefault",
  components: {
    NavBar
  },
  data() {
    return {
      links: [
        {
          to: "/",
          text: "Events"
        },
        {
          to: "/contact",
          text: "Contact"
        }
      ]
    };
  }
};
</script>

<style>
</style>