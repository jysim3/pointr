
<template>
  <div class="nav">
    <div class="box-container">
      <div class="logo">
        <img @click="toHome" class="logo" src="../assets/logo.png" alt="pointr logo" />
      </div>
      <div class="links">
        <router-link
          v-for="(routes, i) in links"
          :key="i"
          :to="routes.to"
          class="link"
        >{{ routes.text }}</router-link>
        <a @click="authBtnClicked" class="btn btn-primary btn--nav">{{ authBtnText }}</a>
      </div>
    </div>
  </div>
</template>
<script>
import { removeToken } from "@/util";
import auth from "@/mixins/auth";

export default {
  name: "NavBar",
  mixins: [auth],
  props: {
    links: {
      type: Array,
      required: false,
      default() {
        return [
          {
            to: "/",
            text: "Events"
          },
          {
            to: "/contact",
            text: "Contact"
          }
        ];
      }
    }
  },
  computed: {
    authBtnText() {
      if (this.userIsAuthenticated) {
        return "Sign out";
      } else {
        return "Sign in";
      }
    }
  },
  methods: {
    authBtnClicked() {
      if (this.userIsAuthenticated) {
        removeToken();
        this.$router.go(0); // TODO: shouldn't need to push a route, should be automatically done by router
      } else {
        this.$router.push({ name: "signIn" });
      }
    },
    toHome() {
      this.$router.push({ name: "home" });
    }
  }
};
</script>
<style scoped>
.nav {
  width: 100%;
  box-shadow: 0 1rem 2rem -1rem rgba(0, 0, 0, 0.2);
  background: #e3f2fd;
  z-index: 1;
  position: relative;
  margin-bottom: 2rem;
  padding: 1.5rem 0 1.5rem 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.box-container {
  width: 80%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.links {
  display: flex;
  justify-content: center;
  align-items: center;
}

.link {
  margin: 0.5rem 2rem 0 2rem;
  font-size: 1.1rem;
}

.link--active {
  box-shadow: inset 0 -2px 0 0 var(--c-secondary-dark);
}

.logo {
  max-width: 200px;
  flex: 1 2 0;
  cursor: pointer;
}

.btn--nav {
  margin-left: 2rem;
  font-size: 1.1rem;
}
</style>