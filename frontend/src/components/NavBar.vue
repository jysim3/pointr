
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
        
        <!-- TODO: Cleaner nav bar would be great -->
      <i class="material-icons routes-icon" :class="{'routes-display-icon': routes.alwaysIcon}">{{ routes.icon }}</i>
        <span class="routes-text" :class="{'routes-display-icon': routes.alwaysIcon}"> {{ routes.text }} </span>
        
        </router-link>
        <!-- TODO: CLEAN UP THIS MESSY SHIT -->
        <div v-if="this.isAuthenticated" class="routes-more-wrapper">
          <i @click="displayMore = !displayMore" class="material-icons routes-display-more">{{ displayMore ? 'expand_less' : 'expand_more' }}</i>

          <transition name="slide-fade">
            <div class="routes-more" v-if="displayMore">
              <router-link :to="'/user/' + this.zID" class="routes-more-profile">
                <img src="https://st3.depositphotos.com/6672868/14376/v/450/depositphotos_143767633-stock-illustration-user-profile-group.jpg"/>
                <div class="routes-more-profile-text">
                  <div class="routes-more-profile-text-title">{{ name }}</div>
                  <span>{{ zID }}</span>
                </div>
              </router-link>
              <hr/>
              <div class="routes-more-link"> Profile </div>
              <div class="routes-more-link"> Change Password </div>
              <div @click="authBtnClicked" class="routes-more-link"> Log out </div>
            </div>
          </transition>
        </div>
        <a v-else @click="authBtnClicked" class="btn btn-primary btn--nav">Sign in</a>


      </div> 
    </div>
  </div>
</template>
<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: "NavBar",
  data() {
    return {
      displayMore: false,
      defaultLinks: [
        {
          to: "/events",
          text: "Events",
          icon: "calendar_today",
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
          icon:"add",
          alwaysIcon: true
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
    ...mapGetters('user', [
      'name', 'zID'
    ]),
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
        this.displayMore = false
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
.routes-display-icon {
  display: block;
}
span.routes-display-icon {
  display: none;
}
.routes-display-more {
  cursor: pointer;
}
.routes-more-wrapper  {
  position: relative;
}
.routes-more  {
  width: 200px;
  position: absolute;
  top: 2rem;
  right: 0;
  background-color: white;
  padding: 1rem;
  border-radius: 5px;
}

.slide-fade-enter-active,.slide-fade-leave-active  {
  transition: all .3s;
}
.slide-fade-enter, .slide-fade-leave-to {
  transform: translateY(-30px);
  opacity: 0;
}

.routes-more-profile {
  display: flex;
  align-items: center;
  box-shadow: none;
}
.routes-more-profile-text {
  margin-left: 1rem;
  display: flex;
  flex-direction: column;
}
.routes-more-profile-text-title {
  font-weight: bold;
  display: block;
  
  color: black;
}
.routes-more-profile > img  {
  width: 50px;
  border-radius: 25px;
} 
.routes-more > hr {
  margin-top: 1rem;
}
.routes-more-link {
  padding-left: 1rem;
  padding-top: 1rem;
  cursor: pointer;
}
.routes-more-link:hover {
  color: black;
  font-weight: bold;
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