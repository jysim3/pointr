
<template>
  <div class="nav">
    <div class="box-container">
      <div class="logo">
        <img @click="toHome" class="logo" src="../assets/logo.png" alt="pointr logo" />
      </div>
      <div v-show="!isLoading" class="routes-container">
        <router-link
          v-for="(routes, i) in navBarLinks"
          :key="i"
          :to="routes.to"
          class="routes"
        >
        
      <i class="material-icons routes-icon">{{ routes.icon }}</i>
        <span class="routes-text"> {{ routes.text }} </span>
        
        </router-link>
        <a @click="authBtnClicked" class="btn btn-primary btn--nav">{{ authBtnText }}</a>
        <a class="routes">
          <i @click="authBtnClicked" class="material-icons routes-icon">{{ authBtnIcon }}</i>
        </a>
      </div> 
    </div>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: "NavBar",
  data() {
    return {
      defaultLinks: [
        {
          to: "/events",
          text: "Events",
          icon: "calendar_today"
        },
        {
          to: "/contact",
          text: "Contact",
          icon: "email"
        }
      ],
      userDashboardLinks: [
        {
          to: "/event",
          text: "Mark attendance",
          icon: "check"
        },
        {
          text: "Societies",
          to: "/societies",
          icon: "pages"
        },
      ],
      adminDashboardLinks: [
        {
          text: "Create Event",
          to: "/create",
          icon:"add"
          
        },
        {
          text: "Societies",
          to: "/society",
          icon: "pages"
        },
        {
          to: "/contact",
          text: "Contact",
          icon: "email"
        }
      ]
    };
  },
  computed: {
    ...mapState('user', {
      isLoading: state => state.isLoading,
      isAuthenticated: state => state.isAuthenticated,
      isAdmin: state => state.isAdmin
    }),
    authBtnIcon() {
      if (this.isAuthenticated) {
        return "exit_to_app";
      } else {
        return "lock";
      }
    },
    authBtnText() {
      if (this.isAuthenticated) {
        return "Sign out";
      } else {
        return "Sign in";
      }
    },
    navBarLinks() {
      if (!this.isAuthenticated) {
        return this.defaultLinks
      }

      if (this.isAdmin) {
        return this.adminDashboardLinks
      } else {
        return this.userDashboardLinks
      }
    }
  },
  methods: {
    ...mapActions('user', [
      'signOut'
    ]),
    authBtnClicked() {
      if (this.isAuthenticated) {
        this.signOut()
        if (this.$route.name !== 'home') {
          // TODO: shouldn't need to push a route, should be automatically done by router. Investigate further, happens when eg sign out from /joinsociety
          this.$router.push({ name: 'home' }); 
        }
      } else {
        // Only want to push if not already on the sign in route.
        if (this.$route.name !== 'signIn') {
          this.$router.push({ name: "signIn" });
        }
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
  padding: 0.4rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-container {
  margin: 0 2rem;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.routes-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.routes {
  margin: 0.5rem 1rem ;
  font-size: 1.1rem;
}

.routes--active {
  box-shadow: inset 0 -2px 0 0 var(--c-secondary-dark);
}
.routes-text {
  display: block;
}
.routes-text, .routes-icon {
  text-align: center;
  width: 100%;
}
.routes-icon {
  display: none;
}

.logo {

  height: 4rem;
  cursor: pointer;
}

.btn--nav {
  margin: 0 2rem 0 2rem;
  font-size: 1rem;
}
@media only screen and (max-width: 900px) {
  
  .routes-icon {
    font-size: 2rem;
  }
  .routes-icon {
    display: inherit;
  }
  .routes-text {
    display: none;
  }
  .btn--nav {
    display: none;
  }
}
@media only screen and (max-width: 700px) {
  .box-container{
    flex-direction: column;
  }
}
</style>