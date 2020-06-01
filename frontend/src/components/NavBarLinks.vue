<template>
<div class="routes-container">
    
        <router-link
          v-for="(routes, i) in navBarLinks"
          :key="i"
          :to="routes.to"
          class="routes link"
        >
          <!-- TODO: Cleaner nav bar would be great -->
          <i
            class="material-icons routes-icon"
          >{{ routes.icon }}</i>
          <span
            class="routes-text"
          >{{ routes.text }}</span>
        </router-link>
        </div>
</template>
<script>
export default {
    name: "NavBarLinks",
    data() {
        return {
            defaultLinks: [
                {
                to: "/event",
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
        }
    },
    computed: {
        navBarLinks() {
        if (!this.$store.getters.isAuthenticated) {
            return this.defaultLinks;
        }
          return this.userDashboardLinks;
        }
    }
}
</script>
<style scoped>

.routes {
  margin: 0.5rem 1rem;
  font-size: 1.1rem;
}

.routes--active {
  box-shadow: inset 0 -2px 0 0 var(--c-secondary-dark);
}
.routes-text {
  color: white;
  display: block;
}
.routes-text,
.routes-icon {
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
</style>