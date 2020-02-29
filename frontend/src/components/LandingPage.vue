<template>
  <div>
    <div class="container">
      <img src="../assets/stockphoto1.png" />
      <div class="right">
        <h1 id="heading">Welcome to Pointr!</h1>
        <h3 id="sub-heading">The event tracking system for UNSW colleges.</h3>
        <div id="btn-container">
          <router-link tag="button" to="/create" class="btn btn-primary">Create an event</router-link>
          <router-link tag="button" to="/sign" class="btn btn-secondary">Mark my attendance</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LandingPage"
};
</script>

<style scoped>
.container {
  width: 80%;
  margin: auto;
  padding-top: 4rem;
  display: flex;
  justify-content: space-between;
}
.left {
  min-width: 0;
}
.right {
  min-width: 0;
}
#heading,
#sub-heading {
  text-align: right;
}

.btn {
  font-size: 1.5rem;
  margin: 0 1rem;
}

#btn-container {
  display: flex;
  justify-content: right;
  margin-top: 7rem;
}
</style>