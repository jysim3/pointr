<template>
  <div>
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

.title{
    color: #f35626;
    background-image: linear-gradient(92deg, #f35626 0%,#feab3a 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: hue 60s infinite linear;
}
.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width:100%;
}
</style>
