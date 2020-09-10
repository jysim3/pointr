
<template>
  <nav class="navbar navbar-expand-lg navbar-dark ">
    <router-link
      class="navbar-brand  mx-0"
      to="/"
    >
      <img
        class="logo"
        src="../assets/logo.png"
        alt="pointr logo"
      >
      (beta)
    </router-link>
    <div class="flex-grow-1 nav-link d-md-block d-none">
      <NavBarSearch class="" />
    </div>
    <button
      class="navbar-toggler"
      type="button"
      @click="show = !show"
    >
      <span
        class="navbar-toggler-icon"
      />
    </button>
    <div
      v-show="show"
      class="collapse navbar-collapse flex-grow-0 show"
    >
      <ul class="navbar-nav">
        <li 
          v-for="(routes, i) in navBarLinks"
          :key="i"
          class="nav-item active"
        >
          <router-link
            :to="routes.to"
            class="nav-link"
          >
            {{ routes.text }}
          </router-link>
        </li>
        <li class="nav-item">
          <NavBarProfile v-if="isAuthenticated" />
          <router-link
            v-else
            to="/signin"
            class="btn btn-primary m-0"
          >
            Sign in
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>
<script>
import NavBarProfile from "@/components/NavBarProfile.vue";
import NavBarSearch from "@/components/NavBarSearch.vue";
import { mapGetters } from "vuex";

export default {
  name: "NavBar",
  components: {
    NavBarProfile, 
    NavBarSearch
  },
  data() {
    return {
      defaultLinks: [
        {
          to: "/event",
          text: "Events",
          icon: "calendar_today"
        },
        {
          to: "/request",
          text: "Contact",
          icon: "email"
        }
      ],
      userDashboardLinks: [
        {
          to: "/event",
          text: "Events",
          icon: "calendar_today"
        },
        {
          text: "Societies",
          to: "/society",
          icon: "pages"
        },
        {
          text: "Create",
          to: "/create",
          icon: "add"
        },
      ],
      displayMore: false,
      show:false
    };
  },
  
  computed: {
    ...mapGetters("user", ["name", "zID"]),
    isAuthenticated() { return this.$store.getters.isAuthenticated},
    isLoading() { return this.$store.getters['user/isLoading']},
    authBtnIcon: () => (this.isAuthenticated ? "exit_to_app" : "lock"),
    navBarLinks() { return !this.$store.getters.isAuthenticated ? this.defaultLinks : this.userDashboardLinks }
  }
};
</script>
<style scoped>
.navbar {
  box-shadow: 0 1rem 2rem -1rem rgba(0, 0, 0, 0.2);
  background: #252525;
  z-index: 1;
}
.logo {
  height: 4rem;
  cursor: pointer;
}
.nav-item{
  text-align: center;
}
</style>