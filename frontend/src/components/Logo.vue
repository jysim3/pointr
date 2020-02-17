<template>
    <div class="img-container">
      <img class="logo" src="../assets/logo.png" alt="pointr logo">
    </div>
</template>

<script>
export default {
    name: 'Logo'
}
</script>

<style scoped>
  .img-container {
    margin: 2rem 0;
    display: flex;
    justify-content: center;
  }

  .logo {
    max-width: 15%;
  }
</style>