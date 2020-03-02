<template>
<div>
  <div id="form-container--signup" class="form-container">
    <form @submit.prevent="submitSignUpForm" class="form">
      <h2>Join Pointr</h2>
      <FormError v-if="formErrorMessage" :msg="formErrorMessage" />
      <InputZID v-model="zID" :zID="zID" />
      <label for="name" class="label">Name</label>
      <input v-model="userInfo.name" class="input" type="text" name="name" />
      <InputPassword v-model="password" :password="password" />
      <InputPassword
        v-model="repeatPassword"
        :password="repeatPassword"
        :label="'Repeat password'"
        :class="{ 'input--invalid': passwordsNotEqual }"
      />
      <!-- TODO: fix :class on repeatPassword input -->
      <label class="label">Year began study</label>
      <input
        v-model.number="userInfo.commencmentYear"
        :max="currentYear"
        :min="2000"
        type="number"
        class="input"
        :class="commencmentYearValid"
        required
      />
      <!-- Degree type input -->
      <label for="degree-type" class="label">Degree type</label>
      <div class="radio-input-container">
        <input
          v-model="userInfo.degreeType"
          :value="'undergraduate'"
          class="input"
          type="radio"
          name="degree-type"
          id="undergraduate"
          required
        />
        <label for="undergraduate" class="label">Undergraduate</label>
      </div>
      <div class="radio-input-container">
        <input
          v-model="userInfo.degreeType"
          :value="'postgraduate'"
          class="input"
          type="radio"
          name="degree-type"
          id="postgraduate"
          required
        />
        <label for="postgraduate" class="label">Postgraduate</label>
      </div>
      <!-- Student type input -->
      <label for="student-type" class="label">Student type</label>
      <div class="radio-input-container">
        <input
          v-model="userInfo.studentType"
          :value="'domestic'"
          type="radio"
          name="student-type"
          id="domestic"
          required
        />
        <label for="domestic" class="label">Domestic</label>
      </div>
      <div class="radio-input-container">
        <input
          v-model="userInfo.studentType"
          :value="'international'"
          type="radio"
          name="student-type"
          id="international"
          required
        />
        <label for="international" class="label">International</label>
      </div>
      <!-- Arc member input -->
      <div class="checkbox-input-container">
        <label for="arc-member">Are you an arc member?</label>
        <input v-model="userInfo.isArcMember" type="checkbox" id="arc-member" name="arc-member" required />
      </div>
      <!-- TODO: gender input? -->
      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>
  </div>
</div>
</template>

<script>
import { fetchAPI, setToken } from "@/util.js";
import FormError from "@/components/FormError.vue";
import InputZID from "@/components/input/InputZID.vue";
import InputPassword from "@/components/input/InputPassword.vue";

export default {
  name: "SignUp",
  components: {
    FormError,
    InputZID,
    InputPassword,
  },
  data() {
    return {
      zID: "",
      password: "",
      repeatPassword: "",
      userInfo: {
        name: "",
        commencmentYear: "",
        studentType: "",
        degreeType: "",
        isArcMember: false
      },
      formErrorMessage: ""
    };
  },
  created() {
    this.userInfo.commencmentYear = this.currentYear;
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
    commencmentYearValid() {
      const year = this.userInfo.commencmentYear;
      let isInvalid = year > 2020 || year < 2000;

      return { "input--invalid": isInvalid };
      // TODO: should computed return a class or should classes be dealth with in the template after computed returns value?
    }
  },
  methods: {
    submitSignUpForm() {
      fetchAPI("/api/auth/register", "POST", {
        zID: this.zID,
        name: this.userInfo.name,
        password: this.password,
        commencementYear: this.userInfo.commencmentYear,
        studentType: this.userInfo.studentType,
        degreeType: this.userInfo.degreeType,
        isArc: this.userInfo.isArcMember
      }).then(r => {
          // In the case of a successful response, want to store token and redirect to home
          if (r.status === 200) {
            setToken(r.data.token)
            this.$router.push({ name: "home" });
            this.$emit('registered', {zid: this.zID, name: this.name})
          } else {
            if (r.data.message["zID"]) {
              this.formErrorMessage = "Please check your zID";
            } else {
              this.formErrorMessage = r.data.message;
            }
          }

      })
    }
  }
};
</script>

<style scoped>
</style>