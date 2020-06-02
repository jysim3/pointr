<template>
  <div class="card-container">
    <div class="form-container" id="form-container--signin">
        <form @submit.prevent="submitReset" class="form">
        <h1>Reset Password</h1>
        <p class="msg" v-if="status === 'success'">
          Thanks for activating your account, you may now close this window or
        </p>
        <div v-else>
          <InputNewPassword v-model="password"  />
            <button type="submit" class="btn btn-primary">Reset Password</button>
        </div>
        </form>
    </div>
  </div>
</template>

<script>
import InputNewPassword from "@/components/input/InputNewPassword.vue";
import axios from 'axios'

export default {
  name: "ResetPassword",
  components: {
      InputNewPassword
  },
  props: {
    forgotToken: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      zID: "",
      password: "",
      oldPassword: "",
      repeatPassword: "",
      status: '',

      error: ""
    };
  },
  methods: {
      async submitReset() {
          const data = {
            password: this.password
          }
          axios({
            url: `/api/auth/reset`,
            method: "POST",
            data: data,
            headers: {
              Authorization: this.activateToken
            }
          }).then(() => {
            this.status = 'success'
          }).catch(e => {
            console.log(e.response)
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