<template>
  <div>
    <div class="form-container" id="form-container--signin">
      <form @submit.prevent="submitSignInForm" class="form">
        <h2>Sign in to Pointr</h2>
        <FormError v-if="error" :msg="error" />
        <InputZID v-model="zID" :zID="zID" />
        <Input v-model="password" type="password" label="Password" />
        <!-- <div class="label-input-div">
        <label class="label input--checkbox-label">Remember me</label>
        <input v-model="rememberUser" class="input input--checkbox" type="checkbox" />
        </div>-->
        <button type="submit" class="btn btn-primary">Sign In</button>
        <div class="additional-links">
          <p>Forgot your password?</p>
          <router-link to="/forgotPassword">Reset your password here</router-link>
          <p>Don't have an account? Sign up </p>
          <router-link id="need-account-link" to="/signup">Sign up here</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util";
import FormError from "@/components/FormError.vue";
import InputZID from "@/components/input/InputZID.vue";
import Input from "@/components/input/Input.vue";
// import InputPassword from "@/components/input/InputNewPassword.vue";

export default {
  name: "SignIn",
  components: {
    FormError,
    InputZID,
    Input
    // InputPassword,
  },
  data() {
    return {
      zID: "",
      password: "",
      // rememberUser: false,
      error: ""
    };
  },
  methods: {
    async submitSignInForm() {
      try {
        await fetchAPI("/api/auth/login", "POST", {
          zID: this.zID,
          password: this.password
        })

        this.$router.push(this.$route.query.redirect || { name: 'home' });
      } catch(error) {
        const errorResponse = error.response;
        if (errorResponse.status === 403) {
          this.error = "Please check your sign in credentials"
        } else {
          this.error = "There was an error when trying to sign you in."
        }
      }
    }
  }
};
</script>

<style scoped>
#form-container--signin {
  margin-top: 2rem;
}

.additional-links {
  margin-top: 2rem;
  text-align: center;
}

.additional-links a {
  margin-bottom: 1rem;
  display: inline-block;
}
.additional-links p {
  padding-bottom: 0.5rem;
}
</style>