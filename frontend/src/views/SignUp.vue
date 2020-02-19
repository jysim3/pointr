<template>
  <div class="form-container">
    <form @submit.prevent="submitSignUpForm" class="form">
      <h2>Join Pointr</h2>
      <div class="label-input-div">
        <label class="label">zID</label>
        <input class="input" type="text" required />
      </div>
      <div class="label-input-div">
        <label class="label">Password</label>
        <input v-model="password" class="input" type="password" required />
      </div>
      <div class="label-input-div">
        <label class="label">Repeat password</label>
        <input
          v-model="repeatPassword"
          :class="{ 'input--invalid': passwordsNotEqual }"
          class="input"
          type="password"
          required
        />
      </div>
      <div class="label-input-div">
        <label class="label">Year began study</label>
        <input
          v-model.number="queryData.comencmentYear"
          :max="currentYear"
          type="number"
          class="input"
          required
        />
      </div>
      <label for="degree-type" class="label">Degree type</label>
      <div class="label-input-div radio-div">
        <input id="undergraduate" type="radio" name="degree-type" required />
        <label for="undergraduate" class="label">Undergraduate</label>
      </div>
      <div class="label-input-div radio-div">
        <input id="postgraduate" type="radio" name="degree-type" required />
        <label for="postgraduate" class="label">Postgraduate</label>
      </div>
      <label for="student-type" class="label">Student type</label>
      <div class="label-input-div radio-div">
        <input id="domestic" type="radio" name="student-type" required />
        <label for="domestic" class="label">Domestic</label>
      </div>
      <div class="label-input-div radio-div">
        <input id="international" type="radio" name="student-type" required />
        <label for="international" class="label">International</label>
      </div>
      <!-- Gender, domestic or international -->
      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "SignUp",
  data() {
    return {
      zID: "",
      password: "",
      repeatPassword: "",
      queryData: {
        degree: "",
        comencmentYear: "",
        degreeType: ""
      }
    };
  },
  created() {
    this.queryData.comencmentYear = this.currentYear
  },
  computed: {
    passwordsNotEqual() {
      // Only want to make input invalid after user has started typing
      if (!this.repeatPassword) {
        return false;
      }
      return this.password !== this.repeatPassword;
    },
    currentYear() {
      const date = new Date();
      return date.getFullYear();
    }
  },
  methods: {
    submitSignUpForm() {}
  }
};
</script>

<style>
</style>