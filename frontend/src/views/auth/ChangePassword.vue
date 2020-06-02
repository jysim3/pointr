<template>
  <div class="card-container">
    <div class="form-container" id="form-container--signin">
        <form @submit.prevent="submitReset" class="form">
        <h1>Change Password</h1>
        <FormMessage :msg="error" />
        <Input v-model="oldPassword" type="password" label="Old Password" />
        <InputNewPassword v-model="password"  />
            <button type="submit" class="btn btn-primary">Reset Password</button>
        </form>
    </div>
  </div>
</template>

<script>
import InputNewPassword from "@/components/input/InputNewPassword.vue";
import FormMessage from '@/components/FormMessage.vue'
import Input from "@/components/input/Input.vue";
import axios from 'axios'

export default {
  name: "ResetPassword",
  components: {
      InputNewPassword, Input,
      FormMessage
  },
  data() {
    return {
      password: "",
      oldPassword: "",
      repeatPassword: "",

      error: {
        success: null,
        message: ""
      }
    };
  },
  methods: {
      async submitReset() {
          const data = {
            password: this.password,
            oldPassword: this.oldPassword
          }
          axios.post('/api/auth/change',data)
          .then(() => {
            this.error.success = true
            this.error.message = "Success"
          })
          .catch(() => {
            this.error.success = false
            this.error.message = "There was an error when trying to sign you in."

          })
      }
  }
};
</script>

<style scoped>
.msg {
  margin-top: 2rem;
}
</style>