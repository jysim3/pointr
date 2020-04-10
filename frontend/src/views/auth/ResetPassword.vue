<template>
  <div class="card-container">
    <div class="form-container" id="form-container--signin">
        <form @submit.prevent="submitReset" class="form">
        <h1>Reset Password</h1>
        <InputNewPassword v-model="password"  />
            <button type="submit" class="btn btn-primary">Reset Password</button>
        </form>
    </div>
  </div>
</template>

<script>
import InputNewPassword from "@/components/input/InputNewPassword.vue";
import { mapMutations } from "vuex";
import jwt from "jsonwebtoken";
import { fetchAPI } from '@/util.js'

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

      error: ""
    };
  },
  async created() {
    try {
      const decodedToken = jwt.decode(this.forgotToken);
      this.zID = decodedToken['zID'];
    } catch (error) {
      this.isActivatedStatus = error.response.status;
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
      try {
        await fetchAPI("/api/auth/reset", "POST", data)
        this.resetState()
        this.$router.push({ name: 'home' });
      } catch(error) {
        console.log(error.response) //eslint-disable-line
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