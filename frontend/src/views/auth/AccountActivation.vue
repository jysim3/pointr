<template>
  <div class="card-container">
    <div class="card">
      <h1>Hi {{ this.name }} ({{ this.zID }})!</h1>
      <p class="msg" v-if="isActivated.status === 200">
        Thanks for activating your account, you may now close this window or
        <router-link to="/signin">sign in</router-link>.
      </p>
      <p class="msg" v-else-if="isActivated.status === 403">
        Your account has already been activated! You can sign in
        <router-link to="/signin">here</router-link>
      </p>
      <p
        class="msg"
        v-else
      >An error was encountered when trying to activate your account. If the issue persists, please <router-link to="/contact">contact us</router-link>. {{ isActivated.msg }}</p>
    </div>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";
import { fetchAPI } from "@/util";

export default {
  name: "AccountActivation",
  props: {
    activateToken: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      zID: "",
      name: "",
      isActivated: {
        status: null,
        msg: ""
      }
    };
  },
  created() {
    const decodedToken = jwt.decode(this.activateToken);
    // this.name = decodedToken["name"]; TODO: need to do an info request
    this.zID = decodedToken["zID"];

    fetchAPI(`/api/auth/activate?token=${this.activateToken}`).then(r => {
      this.isActivated.status = r.status;
      this.isActivated.msg = r.message;
      console.log("r is" + r); //eslint-disable-line
    });
  }
};
</script>

<style scoped>
.msg {
  margin-top: 2rem;
}
</style>