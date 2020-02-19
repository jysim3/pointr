<template>
  <div>
    <Logo />
    <h2 id="heading">The event tracking system for UNSW colleges.</h2>
    <div id="btn-container">
      <button @click="eventCreate" class="btn btn-primary">Create an event</button>
      <button @click="markAttendance" class="btn btn-secondary">Mark my attendance</button>
    </div>
    <div id="admin">
      <a href id="admin-link">I’m administration</a>
    </div>
    <button class="btn btn-primary" @click="signIn">Sign In</button>
  </div>
</template>

<script>
import router from "@/router/index.js";
import Logo from "@/components/Logo.vue";

export default {
  name: "LandingPage",
  components: {
    Logo
  },
  methods: {
    eventCreate() {
      router.push({ name: "create" });
    },
    markAttendance() {
      router.push({ name: "markAttendance" });
    },
    signIn() {
      router.push({ name: "signIn" });
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
  font-size: 1.5rem;
}
</style>