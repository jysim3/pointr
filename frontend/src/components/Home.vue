<template>
  <div id="home-container">
    <div class="center">
      <h1 class="title">Room Pointer</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "../assets/style.css";

#home-container {
  background-color: var(--primary-yellow);
  margin: 0;
  width: 100vw;
  height: 100vh;
}

.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width:100%;
}
</style>
