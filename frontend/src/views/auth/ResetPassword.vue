<template>
  <div class="card-container">
    <div class="form-container" id="form-container--signin">
        <form @submit.prevent="submitReset" class="form">
        <h1>{{forgotToken ? 'Reset ' : 'Change '}} Password</h1>
        <Input v-if="!forgotToken" v-model="oldPassword" label="Old Password" />
        <InputNewPassword v-model="password"  />
            <button type="submit" class="btn btn-primary">Reset Password</button>
        </form>
    </div>
  </div>
</template>

<script>
import InputNewPassword from "@/components/input/InputNewPassword.vue";
import Input from "@/components/input/Input.vue";
import { mapMutations } from "vuex";
import jwt from "jsonwebtoken";
import { fetchAPI } from '@/util.js'

export default {
  name: "ResetPassword",
  components: {
      InputNewPassword, Input
  },
  props: {
    forgotToken: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      zID: "",
      password: "",
      oldPassword: "",
      repeatPassword: "",

      error: ""
    };
  },
  async created() {
    if (this.forgotToken) {
      try {
        const decodedToken = jwt.decode(this.forgotToken);
        this.zID = decodedToken['zID'];
      } catch (error) {
        this.isActivatedStatus = error.response.status;
      }
    }
  },
  methods: {
    ...mapMutations('user', [
      'authToken', 'resetState'
    ]),
      async submitReset() {
          const data = {
            password: this.password
          }
          this.authToken(this.forgotToken);
          if (!this.forgotToken) {
              data.oldPassword = this.oldPassword

          }
      try {
        await fetchAPI("/api/auth/reset", "POST", data)
        this.resetState()

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