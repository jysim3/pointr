<template>
  <div class="container">
    <div class="box">
      <h1>Hi {{ zID }}!</h1>
      <p
        v-if="isActivatedStatus === 200"
        class="msg"
      >
        Thanks for activating your account, you may now close this window or
        <router-link to="/signin">
          sign in
        </router-link>.
      </p>
      <p
        v-else-if="isActivatedStatus === 'loading'"
        class="msg"
      >
        Activating...
      </p>
      <p
        v-else
        class="msg"
      >
        An error was encountered when trying to activate your account. If the issue persists, please <router-link to="/contact">
          contact us
        </router-link>.
      </p>
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
      required: true
    }
  },
  data() {
    return {
      isActivatedStatus: "",
    };
  },
  created() {
    if (this.activateToken) {
      this.isActivatedStatus = "loading"
      const decodedToken = jwt.decode(this.activateToken);
      this.zID = decodedToken ? decodedToken['zID'] : '';
      axios({
        url: `/api/auth/activate`,
        method: "POST",
        headers: {
          Authorization: this.activateToken
        }
      }).then(r => {
        this.isActivatedStatus = r.status;
      }).catch(error => {
        this.isActivatedStatus = error.response.status;
      })
    }
  },
};
</script>

<style scoped>
.msg {
  margin-top: 2rem;
  text-align: center;
}
</style>