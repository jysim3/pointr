<template>
  <div>
    <div class="container">
      <img class="left" src="../assets/stockphoto1.png" />
      <div class="right">
        <h1 class="heading">Welcome to Pointr!</h1>
        <h3 class="sub-heading">The event tracking system for UNSW colleges.</h3>
        <div class="btn-container">
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
.heading,
.sub-heading {
  text-align: right;
}

.btn {
  font-size: 1.5rem;
  margin: 1rem;
}

.btn-container {
  display: flex;
  justify-content: right;
  margin-top: 7rem;
}
@media only screen and (max-width: 600px) {
  .left {
    display: none;
  }
  .heading,.sub-heading{
    text-align: center;
  }
  .btn-container {
    justify-content: center;
    margin: 3rem;
    flex-wrap: wrap;
  }
}
</style>