<template>
  <div class="container">
    <Form
      @submit="submitReset"
    >
      <template #header>
        <h1>Reset Password</h1>
      </template>
      <p
        v-if="status === 'success'"
        class="msg"
      >
        Thanks for activating your account, you may now close this window to sign in
      </p>
      <div v-else>
        <InputNewPassword v-model="password" />
      </div>
      <template #footer>
        <span v-if="status ==='success'"/>
        <button 
          v-else 
          type="submit"
          class="btn btn-primary"
        >
          Reset Password
        </button>
      </template>
    </Form>
  </div>
</template>

<script>
import InputNewPassword from "@/components/input/InputNewPassword.vue";
import axios from 'axios'
import Form from "@/components/Form.vue"

export default {
  name: "ResetPassword",
  components: {
    Form,
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
          Authorization: this.forgotToken
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