<template>
  <div class="card-container">
    <div class="card">
      <h1>Hi {{ this.givenzID }}!</h1>
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
      <Input v-model="zID" type="text" />
      <button v-if="isActivatedStatus === ''" @click="resendActivation" class="btn btn-primary"> Resend Activation Email </button>
      <h3 v-else-if="isActivatedStatus === 'sent'">Success!</h3>
    </div>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";
import Input from "@/components/input/Input";
import axios from "axios";

export default {
  name: "AccountActivation",
  components: {
    Input
  },
  props: {
    givenzID: {
      type:String,
    },
    activateToken: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      // name: "",
      zID: this.givenzID || '',
      isActivatedStatus: "",
    };
  },
  created() {
    if (this.activateToken) {
      this.isActivatedStatus = "loading"
      try {
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
        })
      } catch (error) {
        this.isActivatedStatus = error.response.status;
      }
    }
  },
  methods: {
    resendActivation() {
      axios.post('/api/auth/activate/resend',{}, {
        params: {
          zID: this.zID
        }
      })
      .then(() => {
        this.isActivatedStatus = 'sent'
      }).catch(v => console.log(v))
    }
  }

};
</script>

<style scoped>
.msg {
  margin-top: 2rem;
}
</style>