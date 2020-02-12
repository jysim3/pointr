<template>
  <div class="form-container" id="sign-in-form-container">
    <form @submit.prevent="submitSignInForm" class="form">
      <h2>Sign in to Pointr</h2>
      <div class="label-input-div">
        <label class="label">zID</label>
        <input v-model="zid" class="input" type="text" required />
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
export default {
  name: "SignIn",
  data() {
    return {
      zid: "",
      password: "",
      rememberUser: false
    }
  },
  methods: {
    submitSignInForm() {
      // [zZ][0-9](7)
      // If sign in successfull, push route to profile
      
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