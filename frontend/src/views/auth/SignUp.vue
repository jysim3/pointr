<template>
  <div class="container">
    <Form @submit="submitSignUpForm">
      <template #header>
        <h2>Join Pointr</h2>
        <div class="additional-link">
          <p>Have an account?</p>
          <router-link
            id="need-account-link"
            to="/signin"
          >
            Sign in here
          </router-link>
        </div>
        <FormError
          v-if="formErrorMessage"
          :msg="formErrorMessage"
        />
      </template>
      <InputZID v-model="zID" />
      <Input
        v-model="userInfo.firstName"
        name="firstName"
        type="text"
        label="First Name"
      />
      <Input
        v-model="userInfo.lastName"
        name="lastName"
        type="text"
        label="Last Name"
      />

      <InputPassword v-model="password" />
      <!-- 
      <Input
        v-model="userInfo.discord"
        name="discord"
        type="text"
        label="Discord Username (optional)"
      /> -->
      <Input 
        v-model="userInfo.isArcMember"
        label="Are you an arc member?"
        type="checkbox"
      />

      <template #footer>
        <div class="d-flex flex-column align-items-center">
          <span>By signing up, you agree to our</span>
          <span>
            <router-link :to="{name:'privacy'}">
              privacy policy
            </router-link>
            and
            <router-link :to="{name:'terms'}" >
              terms and condition</router-link>
          </span>
        </div>
        <button
          type="submit"
          :class="['btn', formErrorMessage ? 'btn-warning' : 'btn-primary']"
        >
          Sign Up
        </button>
      </template>
    </Form>
  </div>
  <!-- <Input v-model="userInfo.preferredName" type="text" label="Preferred Name"/> -->
  <!-- TODO: fix :class on repeatPassword input
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
      <Input required 
        label="Degree Type" 
        type="radio" 
        :options="degreeTypeOptions"
        name="degree-type"
        v-model="userInfo.degreeType" />
      <Input required 
        label="Student Type" 
        type="radio" 
        :options="studentTypeOptions"
        name="degree-type"
        v-model="userInfo.studentType" /> -->

  <!-- Arc member input -->
</template>

<script>
import FormError from "@/components/FormError.vue";
import Form from "@/components/Form.vue";
import InputZID from "@/components/input/InputZID.vue";
import Input from "@/components/input/Input.vue";
import InputPassword from "@/components/input/InputNewPassword.vue";

export default {
  name: "SignUp",
  components: {
    FormError,
    Form,
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
        commencmentYear: this.currentYear,
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
  computed: {
    currentYear() {
      const date = new Date();
      return date.getFullYear();
    },
    commencmentYearValid() {
      const year = this.userInfo.commencmentYear;
      let isInvalid = year > 2020 || year < 2000;
      return { "input--invalid": isInvalid };
    }
  },
  methods: {
    submitSignUpForm() {
      const data = {
        zID: this.zID,
        firstName: this.userInfo.firstName,
        lastName: this.userInfo.lastName,
        password: this.password,
        commencementYear: this.userInfo.commencmentYear,
        isArc: this.userInfo.isArcMember
      }
      this.$store.dispatch('auth/register',data)
        .then(() => {
          // In the case of a successful response, want to store token and redirect to home
          this.$router.push({ name: "sendActivationEmail" , query: {givenzID: this.zID}});
        }).catch(r => {
          console.log(r.response)
          this.formErrorMessage = Object.values(r.response.data.message)[0]
          console.log(r.response) //eslint-disable-line
        })
    }
  }
};
</script>

<style scoped>
</style>