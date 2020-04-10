<template>
  <div>
    <div class="form-container" id="form-container--signin">
      <form @submit.prevent="submitForgetPassword" class="form">
        <h2>Reset your password</h2>
        <FormError v-if="error" :msg="error" />
        <!-- TODO: style -->
        <InputZID v-model="zID" :zID="zID" />
        <button type="submit" class="btn btn-primary">Reset Password</button>

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

export default {
  name: "ForgetPassword",
  components: {
    FormError,
    InputZID,
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
    async submitForgetPassword() {
      try {
        const response = await fetchAPI("/api/auth/forgot", "POST", {
          zID: this.zID,
        })

        this.$router.push({ name: 'activate' });
        this.authenticateUser(response.data.token);
      } catch(error) {
        // const errorResponse = error.response;
        // if (errorResponse.status === 403) {
        // }
        this.error = "There was an error when trying to reset your password."
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
