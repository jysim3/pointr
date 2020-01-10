<template>
  <div>
    <!-- <div id="container">
      <div id="content">
        <button @click="createEvent" id="create-event-btn" class="home-button">Create event</button>
        <form @submit="submitForm">
          <div class="label-input-div">
            <label class="label" for>Enter attendance</label>
            <input class="input" placeholder="Event code" v-model="eid" type="text" />
          </div>
          <button type="submit" class="home-button" id="submit-id">
            <i class="material-icons">arrow_forward</i>
          </button>
        </form>
      </div>
    </div> -->
    <Logo />
    <h2 id="heading">The event tracking system for UNSW colleges.</h2>
    <div id="btn-container">
      <button @click="createEvent" class="btn btn-primary">Create an event</button>
      <button @click="markAttendance" class="btn btn-secondary">Mark my attendance</button>
    </div>
    <div id="admin">
      <a href="" id="admin-link">I’m administration</a>
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
  methods: {
    createEvent() {
      router.push({ name: "create" });
    },
    markAttendance() {
      router.push({ name: "markAttendance" });
    }
  }
};
</script>

<style scoped>
#heading {
  text-align: center;
  margin-top: 2em;
}

.btn {
  font-size: 1.5rem;
  /* TODO: fix alignment, does not seem quite center? */
  margin: 0 4rem;
}

#btn-container {
  display: flex;
  justify-content: center;
  margin-top: 7rem;
}

#admin {
  text-align: center;
  margin-top: 7rem;
}

#admin-link, #admin-link:visited {
  text-decoration: none;
  color: var(--c-secondary-dark);
  transition: border-bottom 0.2s;
  border-bottom: 2px solid var(--c-secondary);
  font-size: 1.5rem;
}

#admin-link:hover {
  border-bottom: 2px solid var(--c-secondary-dark);
}
</style>
