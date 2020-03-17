
<template>
  <div>
    <div id="form-container--entercode" class="form-container">
      <form class="form" @submit.prevent="submitZID">
        <h2>Make Admin</h2>
        <FormError v-show="formErrorMessage" :msg="formErrorMessage" />
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
import FormError from "@/components/FormError.vue";

export default {
  name: "EventSignEnterCode",
  components: {
    FormError,
  },
  props:{
    socID: {
      type: String
    }
  },
  data() {
    return {
      zID: "",
      formErrorMessage: "",
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
            console.log(r) //eslint-disable-line
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
