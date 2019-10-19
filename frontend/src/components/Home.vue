<template>
  <div id="home-container">
    <!-- <h1 class="title">Room Pointer</h1> -->
    <div class="img-container">
      <img src="../assets/logo.png" alt="pointr logo">
    </div>
    <div id="container">
      <div id="content">
      <button @click="createEvent" id="create-event-btn" class="home-button">Create event</button>
      <form @submit="submitForm">
        <div class="label-input-div">
          <label for>Enter attendance</label>
          <input placeholder="Event code" v-model="eid" type="text" />
        </div>
        <button type="submit" class="home-button" id="submit-id">
          <i class="material-icons">arrow_forward</i>
        </button>
      </form>
    </div>
    </div>
    
  </div>
</template>

<script>
import router from "@/router/index.js";
// import Logo from "./Logo.vue";

export default {
  name: "Home",
  data() {
    return {
      eid: ""
    };
  },
  props: {
    msg: String
  },
  methods: {
    submitForm() {
      router.push({ name: "signEvent", params: { eid: this.eid } });
    },
    createEvent() {
      router.push({ name: 'create'})
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "../assets/style.css";

#home-container {
  background-color: var(--primary-yellow);
  margin: 0;
  width: 100vw;
  /* height: 100vh; */
}

#submit-id {
  font-size: 1rem;
}

#container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh;
}

form {
  background-color: transparent;
  box-shadow: none;
  color: white;
  display: inline-block;
  padding-left: 0;
  padding-right: 0;
}

label {
  margin-left: 0.4rem;
}

.home-button {
  margin-top: 1rem;
  border: 2px solid white;
  background-color: transparent;
  color: white;
  padding: 0.5rem 1rem;
  transition: all 0.2s;
  font-size: 1.5rem;
  font-weight: 400;
  display: block;
}

#create-event-btn {
  margin: 0 auto;
}

.home-button:hover {
  color: var(--primary-yellow);
  background-color: white;
}

/* img {
  padding: 2rem;
} */
</style>
