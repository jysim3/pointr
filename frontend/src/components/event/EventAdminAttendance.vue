<template>
    
    <div>
      <div id="event-form-container" class="form-container">
        <!-- TODO: Have forms be their own component with slots? -->
        
        <div id="event-form" >
            <div v-if="signup">
                <Signup @registered="registered" :isPage="false"/>

                <div id="signup-route">
                <p>Have an account?</p>
                <a id="need-account-link" @click="signup = !signup">Sign in</a>
                </div>
            </div>
            <div v-else>
            <form @submit.prevent="submitEventAttendance" class="form">
                <FormError v-if="error.status" :msg="error.msg" />
                <label class="label" for>zID</label>
                <input class="input" v-model="zID" type="text" required />
                <label class="label" for>Name</label>
                <input class="input" v-model="uname" type="text" required />
                <button type="submit" class="btn btn-primary">Sign attendance</button>
            </form>
            <div id="signup-route">
            <p>Don't have an account?</p>
            <a id="need-account-link" @click="signup = !signup">Sign up</a>
            </div>
            </div>
        </div>

      </div>
    </div>
</template>
<script>
import { fetchAPI } from "@/util";
import FormError from "@/components/FormError.vue";
import Signup from "@/views/auth/SignUp.vue";
export default {
    name:"EventAdminAttendance",
    props: {
        eventID: String,
    },
    components: {
        FormError,
        Signup
    },
    data() {
        return ({
            signup: false,
            zID: "",
            uname: "",
            error: {
                status: false,
                msg: ""
            }
        })
    },
  methods: {
    registered(value) {
        console.log(value) //eslint-disable-line
        this.zID = value.zID
        this.uname = value.name
        this.submitEventAttendance()
        this.signup = false
    },
    submitEventAttendance() {
      const data = {
        zID: this.zID,
        name: this.uname,
        eventID: this.eventID
      };
      fetchAPI("/api/event/signAttendanceAdmin", "POST", data)
        .then(() => {
          this.zID = "";
          this.uname = "";
        })
        .catch(err => {
            console.log(err.response) //eslint-disable-line
          this.error.status = true;
          this.error.msg = err.response.data.message;
        });
    },
  }
}
</script>
<style scoped>

#event-form-container {
  display: inline-block;
}
#signup-route {
  text-align: center;
  margin-top: 1rem;
}
</style>