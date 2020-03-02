<template>
  <div>
    <div class="form-container" id="form-container--signin">
      <form @submit.prevent="submitSignInForm" class="form">
        <h2>Sign in to Pointr</h2>
        <FormError v-if="error" :msg="error" />
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
import { mapActions } from 'vuex';
import { fetchAPI } from "@/util";
import FormError from "@/components/FormError.vue";
import InputZID from "@/components/input/InputZID.vue";
import InputPassword from "@/components/input/InputPassword.vue";

export default {
  name: "SignIn",
  components: {
    FormError,
    InputZID,
    InputPassword,
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
    ...mapActions('user', [
      'authenticateUser'
    ]),
    async submitSignInForm() {
      try {
        const response = await fetchAPI("/api/auth/login", "POST", {
          zID: this.zID,
          password: this.password
        })

        if (response.status === 200) {
          this.$router.push({ name: 'home' });
          this.authenticateUser(response.data.token);
        } else if (response.status === 403) {
          this.error = "Please check your sign in credentials"
        } else {
          this.error = "There was an error when trying to sign you in."
        }
      } catch(error) {
        this.error = "There was an error when trying to sign you in."
        console.log(error) //eslint-disable-line
      }
    }
  }
};
</script>

<style scoped>
#form-container--signin {
  margin-top: 2rem;
}

#signup-route {
  margin-top: 2rem;
  text-align: center;
}

#signup-route p {
  margin-bottom: 0.5rem;
}
</style>