
<template>
  <div>
    <div id="form-container--entercode" class="form-container">
      <form class="form" @submit.prevent="submitZID">
        <h2>Make Admin</h2>
        <FormMessage :msg="formStatus"/>
        <label class="label" for>Enter zid:</label>
        <!-- TODO: sanitise input, using quotes does not work -->
        <input class="input" v-model="zID" type="text" required />
        <button  class="btn btn-primary" type="submit">Make admin</button>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from "@/util";
import FormMessage from "@/components/FormMessage.vue";
// import FormError from "@/components/FormError.vue";

export default {
  name: "EventSignEnterCode",
  components: {
    //FormError,
    FormMessage
  },
  props:{
    socID: {
      type: String
    }
  },
  data() {
    return {
      zID: "",
      formStatus: {
        success: null,
        message: '',
      }
    };
  },
  methods: {
    submitZID() {
        const data = {
            zID: this.zID,
            societyID: this.socID
        }
        fetchAPI("/api/soc/makeAdmin", "POST", data)
        .then(r => {
          this.formStatus.success = true
          this.formStatus.message = r.data.status
        })
        .catch(r => {
          this.formStatus.success = false
          this.formStatus.message =  r.response.data.message;
        })
    }
  }
};
</script>

<style scoped>
#form-container--entercode {
  margin-top: 3rem;
}
</style>
