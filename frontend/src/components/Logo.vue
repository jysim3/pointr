<template>
  <div class="logo-container">
    <!-- <router-link to="/">
      <img class="logo" src="../assets/logo.png" alt="pointr logo" />
    </router-link> -->
    <img @click="toHome" class="logo" src="../assets/logo.png" alt="pointr logo" />
  </div>
</template>

<script>
export default {
  name: "Logo",
  methods: {
    toHome() {
      this.$router.push({ name: 'home' })
    }
  }
};
</script>

<style scoped>
.logo-container {
  margin: 2rem 0;
  display: flex;
  justify-content: center;
}

.logo {
  max-width: 15%;
  cursor: pointer;
}
</style>