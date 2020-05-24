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
                }
            ],
            adminDashboardLinks: [
                {
                text: "Create",
                to: "/create",
                icon: "add",
                },
                {
                text: "Societies",
                to: "/society",
                icon: "pages"
                },
            ]
        }
    },
    computed: {
        isAdmin() { return this.$store.getters['user/isAdmin']},
        navBarLinks() {
        if (!this.isAuthenticated) {
            return this.defaultLinks;
        }

        if (this.isAdmin) {
            return this.adminDashboardLinks;
        } else {
            return this.userDashboardLinks;
        }
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