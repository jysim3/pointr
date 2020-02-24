<template>
  <div class="form-container">
    <form @submit.prevent="submitSignUpForm" class="form">
      <h2>Join Pointr</h2>
      <FormError v-if="formErrorMessage" :msg="formErrorMessage" />
      <InputZID v-model="zID" :zID="zID" />
      <InputPassword v-model="password" :password="password" />
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
          :min="2000"
          type="number"
          class="input"
          :class="comencmentYearValid"
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
import { fetchAPI } from "@/util.js";
import FormError from "@/components/FormError.vue";
import InputZID from "@/components/input/InputZID.vue";
import InputPassword from "@/components/input/InputPassword.vue";

export default {
  name: "SignUp",
  components: {
    FormError,
    InputZID,
    InputPassword
  },
  data() {
    return {
      zID: "",
      password: "",
      repeatPassword: "",
      formErrorMessage: "",
      queryData: {
        degree: "",
        comencmentYear: "",
        degreeType: ""
      }
    };
  },
  created() {
    this.queryData.comencmentYear = this.currentYear;
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
    },
    comencmentYearValid() {
      const year = this.queryData.comencmentYear;
      let isInvalid = year > 2020 || year < 2000;

      return { "input--invalid": isInvalid };
      // TODO: should computed return a class or should classes be dealth with in the template after computed returns value?
    }
  },
  methods: {
    submitSignUpForm() {
      fetchAPI("/api/auth/register", "POST", {
        zID: this.zID,
        password: this.password
      }).then(r => {
        if (r.status !== 200) {
          console.log("r is ", r); //eslint-disable-line
          console.log(r.message["zID"]); //eslint-disable-line
          if (r.message["zID"]) {
            this.formErrorMessage = "Please check your zID";
          } else {
            this.formErrorMessage = r.message;
          }
        } else {
          // In the case of a successful response, want to store token and redirect to home
          localStorage.setItem("token", r.token);
          this.$route.push({ name: "home" });
          console.log("r is ", r); //eslint-disable-line
        }
      });
    }
  }
};
</script>

<style>
</style>