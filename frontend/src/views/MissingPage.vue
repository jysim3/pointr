<template>
  <div class="card-container">
    <div class="card">
      <h1>404 Not Found</h1>
      <p
        class="msg"
      >Seems like you've found something special, but not so special cause this doesn't exist</p>
      <p class="msg" >If you think this is a bug, contact us 
        <router-link :to="{name:'request',params:{request:'bug'}}"> here </router-link> 
      </p>
      <p class="msg" >Click <router-link to="/">here</router-link> to go to the home page</p>
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