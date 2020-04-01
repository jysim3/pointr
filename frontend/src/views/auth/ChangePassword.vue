<template>
  <div class="card-container">
    <div class="form-container" id="form-container--signin">
        <form @submit.prevent="submitReset" class="form">
        <h1>Change Password</h1>
        <Input v-model="oldPassword" type="password" label="Old Password" />
        <InputNewPassword v-model="password"  />
            <button type="submit" class="btn btn-primary">Reset Password</button>
        </form>
    </div>
  </div>
</template>

<script>
import InputNewPassword from "@/components/input/InputNewPassword.vue";
import Input from "@/components/input/Input.vue";
import { fetchAPI } from '@/util.js'

export default {
  name: "ResetPassword",
  components: {
      InputNewPassword, Input
  },
  data() {
    return {
      password: "",
      oldPassword: "",
      repeatPassword: "",

      error: ""
    };
  },
  methods: {
      async submitReset() {
          const data = {
            password: this.password,
            oldPassword: this.oldPassword
          }
      try {
        await fetchAPI("/api/auth/changePassword", "POST", data)
        this.$router.push({ name: 'home' });
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
.msg {
  margin-top: 2rem;
}
</style>