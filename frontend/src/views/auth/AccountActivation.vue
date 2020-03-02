<template>
  <div class="card-container">
    <div class="card">
      <h1>Hi {{ this.$store.state.user.name }} ({{ this.$store.state.user.zID }})!</h1>
      <p v-if="!activateToken">Please go to your email to activate your account first.</p>
      <p class="msg" v-if="isActivatedStatus === 200">
        Thanks for activating your account, you may now close this window or
        <router-link to="/signin">sign in</router-link>.
      </p>
      <p class="msg" v-else-if="isActivatedStatus === 403">
        Your account has already been activated! You can sign in
        <router-link to="/signin">here</router-link>
      </p>
      <p
        class="msg"
        v-else
      >An error was encountered when trying to activate your account. If the issue persists, please <router-link to="/contact">contact us</router-link>.</p>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util";

export default {
  name: "AccountActivation",
  props: {
    activateToken: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      zID: "",
      name: "",
      isActivatedStatus: "",
    };
  },
  async created() {
    if (this.activateToken) {
      try {
        const response = await fetchAPI(`/api/auth/activate?token=${this.activateToken}`, "POST")
        this.isActivatedStatus = response.status;
        this.isActivated.msg = response.data.message;
      } catch (error) {
        this.isActivatedStatus = error.response.status;
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