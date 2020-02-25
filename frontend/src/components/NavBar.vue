
<template>
    <div class="nav">
      <div class="box-container">
        <div class="logo">
            <img @click="toHome" class="logo" src="../assets/logo.png" alt="pointr logo" />
        </div>
        <div class="links-group">
          <router-link v-for="(routes, i) in links"
          :key="i"
          :to="routes.page"
          active-class="active"
          class="link"
          >
          {{routes.text}}
          </router-link>

        </div>
        <div>
        <router-link tag="button" to="/signin" class="btn btn-primary signup-btn">Sign In</router-link>
        </div>
      </div>
    </div>
</template>
<script>
//import Logo from "@/components/Logo.vue";

export default {
name: "NavBar",
  components: {
      //Logo
  },

  methods: {
    toHome() {
      this.$router.push({ name: 'home' })
    }
  },
  data: () => ({
    links: [
      {
        page: '',
        text: 'Events'
      },
      {
        page: '/contact',
        text: 'Contact'
      },
    ]
  })
}
</script>
<style scoped>
.nav {
  width: 100%;
  box-shadow:   0 1rem 2rem -1rem rgba(0, 0, 0, 0.2); 
  background: #e3f2fd;
  z-index: 1;
  position: relative;
  margin-bottom: 2rem;
  padding-top: 20px;
  padding-bottom: 10px;
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
.links-group {
    margin-left: 30px;
    flex: 2 2 0;
    display: flex;
  justify-content: center;
  align-items: center;
}
.link {
    min-width: 200px;
  color: black;
  font-weight: bold;
  margin: 0 15px;
  text-align: center;
}
.active {
  color: #311b92;
}
.logo {
    max-width: 200px;
    flex: 1 1 0;
  cursor: pointer;
}
.signup-btn {
    width: 200px;
}
</style>