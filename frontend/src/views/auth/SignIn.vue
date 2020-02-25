<template>
  <div class="form-container" id="sign-in-form-container">
    <form @submit.prevent="submitSignInForm" class="form">
      <h2>Sign in to Pointr</h2>
      <FormError v-if="error.status" :msg="error.msg" />
      <InputZID v-model="zID" :zID="zID" />
      <InputPassword v-model="password" :password="password" />
      <div class="label-input-div">
        <label class="label input--checkbox-label">Remember me</label>
        <input v-model="rememberUser" class="input input--checkbox" type="checkbox" />
      </div>
      <button type="submit" class="btn btn-primary">Sign In</button>
      <!-- TODO: add button for sign up -->
      <p>Need an account?</p>
      <router-link to="/signup">Sign up</router-link>
    </form>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import FormError from "@/components/FormError.vue";
import InputZID from "@/components/input/InputZID.vue";
import InputPassword from "@/components/input/InputPassword.vue";

export default {
  name: "SignIn",
  components: {
    FormError,
    InputZID,
    InputPassword
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
          if (r.status !== 200) {
            this.error.status = true;
            this.error.msg = "Invalid credentials";
          } else {
            this.$router.push({ name: "home" });
          }
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
</style>