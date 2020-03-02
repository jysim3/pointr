
<template>
  <div class="nav">
    <div class="box-container">
      <div class="logo">
        <img @click="toHome" class="logo" src="../assets/logo.png" alt="pointr logo" />
      </div>
      <div class="links">
        <router-link
          v-for="(routes, i) in navBarLinks"
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
export default {
  name: "NavBar",
  data() {
    return {
      defaultLinks: [
        {
          to: "/",
          text: "Events"
        },
        {
          to: "/contact",
          text: "Contact"
        }
      ],
      userDashboardLinks: [
        {
          to: "/sign",
          text: "Mark attendance"
        },
        {
          to: "/joinsociety",
          text: "Join a society"
        }
      ],
      adminDashboardLinks: [
        {
          text: "Create an event",
          to: "/create"
        },
        {
          text: "Join a society",
          to: "/joinsociety"
        },
        {
          text: "Documentation",
          to: "/documentation"
        },
        {
          text: "Statistics",
          to: "/"
        }
      ]
    };
  },
  computed: {
    authBtnText() {
      if (this.$store.user.isAuthenticated) {
        return "Sign out";
      } else {
        return "Sign in";
      }
    },
    navBarLinks() {
      if (this.$store.user.isAuthenticated) {
        return this.defaultLinks
      }

      if (this.$store.user.isAdmin) {
        return this.adminDashboardLinks
      } else {
        return this.userDashboardLinks
      }
    }
  },
  methods: {
    authBtnClicked() {
      if (this.userIsAuthenticated) {
        this.$store.user.dispatch('signOut')
        //this.$router.go(0); // TODO: shouldn't need to push a route, should be automatically done by router
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
  justify-content: space-between;
  align-items: center;
}

.box-container {
  width: 80%;
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.links {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
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
  cursor: pointer;
}

.btn--nav {
  margin: 0 2rem 0 2rem;
  font-size: 1.1rem;
}
</style>