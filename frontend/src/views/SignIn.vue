<template>
  <div class="form-container" id="sign-in-form-container">
    <form @submit.prevent="submitSignInForm" class="form">
      <h2>Sign in to Pointr</h2>
      <FormError v-if="error.status" :msg="error.msg" />
      <div class="label-input-div">
        <label class="label">zID</label>
        <input v-model="zID" class="input" type="text" required />
      </div>
      <div class="label-input-div">
        <label class="label">Password</label>
        <input v-model="password" class="input" type="password" required />
      </div>
      <div class="label-input-div">
        <label class="label">Remember me</label>
        <input v-model="rememberUser" class="input input-checkbox" type="checkbox" />
      </div>
      <button type="submit" class="btn btn-primary">Sign In</button>
    </form>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js"
import FormError from "@/components/FormError.vue"

export default {
  name: "SignIn",
  components: {
    FormError
  },
  data() {
    return {
      zID: "",
      password: "",
      rememberUser: false,
      error: {
        status: false,
        msg: ""
      }
    }
  },
  methods: {
    submitSignInForm() {
      // [zZ][0-9](7)
      // If sign in successfull, push route to profile
      fetchAPI("/api/auth/login", "POST", {
        "zID": this.zID,
        "password": this.password
      })
      .then(r => {
        if (r.status === 403) {
          this.error.status = true
          this.error.msg = "Please check your zID and password"
        }
      })
      .catch(err => {
        this.error.status = true
        this.error.msg = `Error has occured: ${err}`
      })
    }
  }
};
</script>

<style scoped>
#sign-in-form-container {
  height: 100vh; /* TODO: TEMPORARY FIX DOES NOT WORK WELL WITH SMALLER SCREENS */
  margin: auto 0;
}
</style>