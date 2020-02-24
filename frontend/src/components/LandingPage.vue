<template>
  <div>
    <Logo />
    <h2 id="heading">The event tracking system for UNSW colleges.</h2>
    <div id="btn-container">
      <router-link tag="button" to="/create" class="btn btn-primary">Create an event</router-link>
      <router-link tag="button" to="/mark-attendance" class="btn btn-secondary">Mark my attendance</router-link>
    </div>
    <div id="admin">
      <a href id="admin-link">I’m administration</a>
    </div>
    <router-link tag="button" to="/signin" class="btn btn-primary">Sign In</router-link>
  </div>
</template>

<script>
import Logo from "@/components/Logo.vue";

export default {
  name: "LandingPage",
  components: {
    Logo
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