<template>
  <li
    class="nav-item dropdown" 
    @focusout="show = false"
  >
    <a
      class="nav-link dropdown-toggle"
      href="#"
      role="button"
      @click="show = !show"
    />
    <transition
      name="fade"
      mode="out-in"
    >
      <div
        v-show="show"
        class="dropdown-menu dropdown-menu-right show"
        aria-labelledby="navbarDropdownMenuLink"
        @click="show = false"
      >
        <router-link
          :to="'/user/' + zID"
          class="dropdown-item d-flex"
        >
          <img
            src="@/assets/defaultUser.jpg"
          >
          <div class="routes-more-profile-text">
            <div class="routes-more-profile-text-title">
              {{ name }}
            </div>
            <span>{{ zID }}</span>
          </div>
        </router-link>
        <div class="dropdown-divider" />

        <router-link
          :to="'/user/' + zID"
          class="dropdown-item"
        >
          Profile
        </router-link>
        <router-link
          :to="{name:'changePassword'}"
          class="dropdown-item"
        >
          Change Password
        </router-link>
        <router-link
          :to="'/request'"
          class="dropdown-item"
        >
          Contact
        </router-link>
        <a
          class="dropdown-item"
          href="#"
          @click="signOut"
        >
          Log out
        </a>
      </div>
    </transition>
  </li>
</template>
<script>
export default {
  name: "NavBarProfile",
  data(){ return{ 
    show: false
  }},
  computed: {
    zID () {  return this.$store.getters['user/zID'] },
    name () { return this.$store.getters['user/name'] }
  },
  methods: {
    signOut() { 
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.go('/')
        })
    },
    toggleMore(b){
      this.displayMore = b
      this.$nextTick(() => {
        if (this.displayMore) {
          this.$refs["routes-more"].focus();
        }
      })
    },
  }
    
}
</script>
<style scoped>
.dropdown-toggle:after {
  color: var(--c-primary)
}
.dropdown-item.active, .dropdown-item:active {
    color: #fff;
    text-decoration: none;
    background-color: var(--c-primary)
}
.dropdown-item > img {
  width: 50px;
  border-radius: 25px;
}
</style>