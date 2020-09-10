<template>
  <div class="container">
    <Form
      @submit="submitForgetPassword"
    >

      <template #header>
        <h2>Reset your password</h2>
        <FormMessage :msg="error" />
      </template>
      <InputZID
        v-model="zID"
        :z-i-d="zID"
      />
      <template #footer>
        <button
          type="submit"
          class="btn btn-primary"
        >
          Reset Password
        </button>

        <div id="signup-route">
          <p>Don't have an account?</p>
          <router-link
            id="need-account-link"
            to="/signup"
          >
            Sign up
          </router-link>
        </div>
      </template>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import FormMessage from "@/components/FormMessage.vue";
import InputZID from "@/components/input/InputZID.vue";
import Form from "@/components/Form.vue"

export default {
  name: "ForgetPassword",
  components: {
    FormMessage,
    InputZID,
    Form
  },
  data() {
    return {
      zID: "",
      password: "",
      // rememberUser: false,
      error: {
        message:"",
        success: ""
      },
      status: ''
    };
  },
  methods: {
    submitForgetPassword() {
      axios.post('/api/auth/forgot', {}, {
        params:{
          zID: this.zID
        }
      }).then(() => {

        this.error.success = true
        this.error.message = "Success"
      }) .catch((error) => {
        console.log(error)
        this.error.message = "There was an error when trying to reset your password."
        this.error.success = false
      })
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
