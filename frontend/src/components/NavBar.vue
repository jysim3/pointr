
<template>
  <div class="nav">
    <div class="box-container">
      <div class="logo">
        <router-link to="/">
          <img class="logo" src="../assets/logo.png" alt="pointr logo" />
        </router-link>
      </div>
      <NavBarSearch />
      <div class="routes-container">
        <NavBarLinks />
        <NavBarProfile v-if="this.isAuthenticated" />
        <!-- <router-link v-else to="/signin" class="btn btn-primary btn--nav">Sign in</router-link> -->
        <router-link v-else to="/signup" class="btn btn-primary btn--nav">Sign up</router-link>
      </div>
    </div>
  </div>
</template>
<script>
import NavBarProfile from "@/components/NavBarProfile.vue";
import NavBarLinks from "@/components/NavBarLinks.vue";
import NavBarSearch from "@/components/NavBarSearch.vue";
import { mapGetters } from "vuex";

export default {
  name: "NavBar",
  components: {
    NavBarProfile, NavBarLinks, NavBarSearch
  },
  data() {
    return {
      displayMore: false,
    };
  },
  computed: {
    ...mapGetters("user", ["name", "zID"]),
    isAuthenticated() { return this.$store.getters.isAuthenticated},
    isLoading() { return this.$store.getters['user/isLoading']},
    authBtnIcon: () => (this.isAuthenticated ? "exit_to_app" : "lock"),
  }
};
</script>
<style scoped>
.nav {
  width: 100%;
  box-shadow: 0 1rem 2rem -1rem rgba(0, 0, 0, 0.2);
  background: #252525;
  z-index: 1;
  position: relative;
  /* margin-bottom: 2rem; */
  padding: 0.4rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-container {
  margin: 0 2rem;
  width: 100%;
  display: flex;
  justify-content: stretch;
  align-items: center;
  flex-wrap: wrap;
}
.box-container > div {
  flex: 1 1 auto;
}

.routes-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex-wrap: wrap;
}

.logo {
  height: 4rem;
  cursor: pointer;
}

@media only screen and (max-width: 900px) {
  .searchBar {
    display: none;
  }
  .routes-icon {
    font-size: 2rem;
  }
  .routes-icon {
    display: inherit;
  }
  .routes-text {
    display: none;
  }
}
@media only screen and (max-width: 700px) {
  .box-container {
    flex-direction: column;
  }
  .routes-container {
    justify-content: center;
  }
}
</style>