<template>
<div>
  <div id="form-container--signup" class="form-container">
    <form @submit.prevent="submitSignUpForm" class="form">
      <h2>Join Pointr</h2>
      <FormError v-if="formErrorMessage" :msg="formErrorMessage" />

      <InputZID v-model="zID"  />

      <Input v-model="userInfo.firstName" type="text" label="First Name"/>
      <Input v-model="userInfo.lastName" type="text" label="Last Name"/>
      <Input v-model="userInfo.preferredName" type="text" label="Preferred Name"/>

      <InputPassword v-model="password"  />
      <!-- TODO: fix :class on repeatPassword input -->
      <label class="label">Year began study</label>
      <input
        v-model.number="userInfo.commencmentYear"
        :max="currentYear"
        :min="currentYear-15"
        type="number"
        class="input"
        :class="commencmentYearValid"
        required
      />
      <!-- Degree type input -->
      <Input required 
        label="Degree Type" 
        type="radio" 
        :options="degreeTypeOptions"
        name="degree-type"
        v-model="userInfo.degreeType" />
      <!-- Student type input -->
      <Input required 
        label="Student Type" 
        type="radio" 
        :options="studentTypeOptions"
        name="degree-type"
        v-model="userInfo.studentType" />

      <!-- Arc member input -->
      <Input required
        label="Are you an arc member?"
        v-model="userInfo.isArcMember"
        type="checkbox"
        />

      <!-- TODO: gender input? -->
      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>
  </div>
</div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import FormError from "@/components/FormError.vue";
import InputZID from "@/components/input/InputZID.vue";
import Input from "@/components/input/Input.vue";
import InputPassword from "@/components/input/InputNewPassword.vue";

export default {
  name: "SignUp",
  components: {
    FormError,
    InputZID,
    InputPassword,
    Input
  },
  props: {
    isPage: {
      type: Boolean,
      default: true
    },
  },
  // TODO: signup page vs event page sign up HACK
  data() {
    return {
      zID: "",
      password: "",
      userInfo: {
        firstName: "",
        lastName: "",
        preferredName: "",
        commencmentYear: "",
        studentType: "",
        degreeType: "",
        isArcMember: false
      },
      studentTypeOptions: [
        { value:'domestic', 'label': 'Domestic'},
        { value:'international', 'label': 'International'}
      ],
      degreeTypeOptions: [
        { value:'undergraduate', 'label': 'Undergraduate'},
        { value:'postgraduate', 'label': 'Postgraduate'}
      ],
      formErrorMessage: "",
    };
  },
  created() {
    this.userInfo.commencmentYear = this.currentYear;
  },
  computed: {
    passwordTooShort() {
      return this.password.length < 8
    },
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
      if (this.passwordTooShort) {

        this.formErrorMessage = "Entered password must be eight characters.";
      } else if (this.passwordsNotEqual) {
        this.formErrorMessage = "Please check your entered password";
        return
      }
      fetchAPI("/api/auth/register", "POST", {
        zID: this.zID,
        firstName: this.userInfo.firstName,
        lastName: this.userInfo.lastName,
        preferredName: this.userInfo.preferredName,
        password: this.password,
        commencementYear: this.userInfo.commencmentYear,
        // studentType: this.userInfo.studentType,
        // degreeType: this.userInfo.degreeType,
        isArc: this.userInfo.isArcMember
      }).then(r => {
          // In the case of a successful response, want to store token and redirect to home
          if (r.status === 200) {
            // TODO: signup page vs event page sign up HACK
            if (this.isPage) {
              this.$router.push({ name: "activate" , params: {zID: this.zID, name: this.name}});
            } else {
              this.$emit('registered', {zID: this.zID, name: this.userInfo.name})
            }
          } 
      }).catch(r => {
            console.log(r.response) //eslint-disable-line
            if (r.response.data.message["zID"]) {
              this.formErrorMessage = "Please check your zID";
            } else {
              this.formErrorMessage = r.data.message;
            }
      })
    }
  }
};
</script>

<style scoped>
</style>