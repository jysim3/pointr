<template>
  <div id="home-container">
    <!-- <div id="container">
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
    </div> -->
    <Logo />
    <h2 class="heading">The event tracking system for UNSW colleges.</h2>
    <div class="btn-container">
      <button @click="createEvent" class="btn-primary btn">Create an event</button>
      <button class="btn-secondary btn">Mark my attendence</button>
    </div>
    <div class="admin">
      <a href="" class="admin-link">I’m administration</a>
    </div>
  </div>
</template>

<script>
import router from "@/router/index.js";
import Logo from "@/components/Logo.vue";

export default {
  name: "Home",
  components: {
    Logo
  },
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
      router.push({ name: "create" });
    }
  }
};
</script>

<style scoped>
@import "../assets/style.css";

.btn-container .btn {
  font-size: 1.5rem;
  /* TODO: fix alignment, does not seem quite center? */
  margin: 0 4rem;
}

.btn-container {
  display: flex;
  justify-content: center;
  margin-top: 7rem;
}

.heading {
  text-align: center;
  margin-top: 2em;
}

.admin {
  text-align: center;
  margin-top: 7rem;
}

.admin-link, .admin-link:visited {
  text-decoration: none;
  color: var(--dark-grey);
  transition: border-bottom 0.2s;
  border-bottom: 2px solid var(--bgc-grey);
  font-size: 1.5rem;
}

.admin-link:hover {
  border-bottom: 2px solid var(--dark-grey);
}
</style>
