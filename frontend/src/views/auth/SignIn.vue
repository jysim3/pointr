<template>
<div>
  <NavBar />
  <div class="form-container" id="sign-in-form-container">
    <form @submit.prevent="submitSignInForm" class="form">
      <h2>Sign in to Pointr</h2>
      <FormError v-if="error.status" :msg="error.msg" />
      <InputZID v-model="zID" :zID="zID" />
      <InputPassword v-model="password" :password="password" />
      <!-- <div class="label-input-div">
        <label class="label input--checkbox-label">Remember me</label>
        <input v-model="rememberUser" class="input input--checkbox" type="checkbox" />
      </div>-->
      <button type="submit" class="btn btn-primary">Sign In</button>
      <div id="signup-route">
        <p>Don't have an account?</p>
        <router-link id="need-account-link" to="/signup">Sign up</router-link>
      </div>
    </form>
  </div>
</div>
</template>

<script>
import { fetchAPI, setToken } from "@/util.js";
import FormError from "@/components/FormError.vue";
import InputZID from "@/components/input/InputZID.vue";
import InputPassword from "@/components/input/InputPassword.vue";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "SignIn",
  components: {
    FormError,
    InputZID,
    InputPassword,
    NavBar
  },
  data() {
    return {
      zID: "",
      password: "",
      rememberUser: false,
      error: {
        status: false,
        msg: ""
      }
    };
  },
  methods: {
    submitSignInForm() {
      fetchAPI("/api/auth/login", "POST", {
        zID: this.zID,
        password: this.password
      })
        .then(r => {
          console.log(r) //eslint-disable-line
          setToken(r.token)
          this.$router.push({ name: "home" });
        })
        .catch(err => {
          this.error.status = true;
          this.error.msg = err;
        });
    }
  }
};
</script>

<style scoped>
#sign-in-form-container {
  height: 100vh; /* TODO: TEMPORARY FIX DOES NOT WORK WELL WITH SMALLER SCREENS */
  margin: auto 0;
}

#signup-route {
  margin-top: 2rem;
  text-align: center;
}

#signup-route p {
  margin-bottom: 0.5rem;
}
</style>