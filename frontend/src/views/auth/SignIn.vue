<template>
  <div class="container">
    <Form
      @submit="submitSignInForm"
    >
      <template #header>
        <h2>Sign in to Pointr</h2>
        <FormError
          v-if="error"
          :msg="error"
        />
      </template>
      <InputZID
        v-model="zID"
        :z-i-d="zID"
      />
      <Input
        v-model="password"
        type="password"
        name="password"
        label="Password"
      />
      <template #footer>
        <button
          type="submit"
          class="btn btn-primary"
        >
          Sign In
        </button>
        <div class="additional-links d-flex flex-column align-items-center">
          <span>Forgot your password?</span>
          <router-link to="/forgotPassword">
            Reset your password here
          </router-link>
          <span>Don't have an account? Sign up</span>
          <router-link
            id="need-account-link"
            to="/signup"
          >
            Sign up here
          </router-link>
        </div>
      </template>
    </Form>
  </div>
</template>

<script>
import FormError from "@/components/FormError.vue";
import InputZID from "@/components/input/InputZID.vue";
import Input from "@/components/input/Input.vue";
import Form from "@/components/Form.vue"

export default {
  name: "SignIn",
  components: {
    Form,
    FormError,
    InputZID,
    Input
  },
  data() {
    return {
      zID: "",
      password: "",
      nextRoute: this.$route.query.redirect || "/",
      error: ""
    };
  },
  computed: {
    isAuthenticated: function() {
      return this.$store.getters.isAuthenticated;
    }
  },
  mounted() {
    if (this.isAuthenticated) {
      this.$router.push(this.nextRoute);
    }
  },
  methods: {
    submitSignInForm() {
      const data = {
        zID: this.zID,
        password: this.password
      };
      this.$store
        .dispatch("login", data)
        .then(() => {
          this.$router.push(this.nextRoute);
        })
        .catch(e => {
          if (e.response) {
            this.error = e.response.data.message;
          }
        });
    }
  }
};
</script>

<style scoped>
</style>