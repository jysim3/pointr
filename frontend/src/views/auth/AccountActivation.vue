<template>
  <div class="card-container">
    <div class="card">
      <h1>Hi {{ this.zID }}!</h1>
      <p class="msg" v-if="!activateToken">Check your zID email to activate your account!</p>
      <p class="msg" v-else-if="isActivatedStatus === 200">
        Thanks for activating your account, you may now close this window or
        <router-link to="/signin">sign in</router-link>.
      </p>
      <p class="msg" v-else-if="isActivatedStatus === 'loading'"> Activating... </p>
      <p
        class="msg"
        v-else
      >An error was encountered when trying to activate your account. If the issue persists, please <router-link to="/contact">contact us</router-link>.</p>
    </div>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";
import axios from "axios";

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
      // name: "",
      zID: '',
      isActivatedStatus: "",
    };
  },
  created() {
    if (this.activateToken) {
      this.isActivatedStatus = "loading"
      try {
        const decodedToken = jwt.decode(this.activateToken);
        this.zID = decodedToken ? decodedToken['zID'] : '';

        // FIXME: VERY HACKY
        axios({
          url: `/api/auth/activate`,
          method: "POST",
          headers: {
            Authorization: this.activateToken
          }
        }).then(r => {
          this.isActivatedStatus = r.status;
        })
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