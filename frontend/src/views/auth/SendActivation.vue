<template>
  <div class="container">
    <div class="box">
      <h1>Hi {{ givenzID }}!</h1>
      <div>
        <p class="msg">
          Check your zID email to activate your account!
        </p>
        <p class="msg">
          Due to UNSW spam filter, your email might take 1-2 minutes to arrive.
        </p>
      </div>
      <Input
        v-model="zID"
        :disabled="givenzID !== undefined"
        type="text"
      />
      <button
        v-if="status === ''"
        class="btn btn-primary"
        @click="resendActivation"
      >
        Resend Activation Email
      </button>
      <h3 v-else-if="status === 'sent'">
        Success!
      </h3>
    </div>
  </div>
</template>

<script>
import Input from "@/components/input/Input";
import axios from 'axios'
export default {
  name: "AccountActivation",
  components: {
    Input
  },
  props: {
    givenzID: {
      type:String,
      default: ''
    },
  },
  data() {
    return {
      // name: "",
      zID: this.givenzID || '',
      status: '',
    };
  },
  methods: {
    resendActivation() {
      axios.post('/api/auth/activate/resend',{}, {
        params: {
          zID: this.zID
        }
      })
        .then(() => {
          this.status = 'sent'
        }).catch(v => console.log(v))
    }
  }
}
</script>

<style>

</style>