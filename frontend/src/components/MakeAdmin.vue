
<template>
  <div
    class="box"
  >
    <form
      class="d-flex flex-column align-items-center"
      @submit.prevent="submitZID"
    >
      <h2>Make Admin</h2>
      <FormMessage :msg="formStatus" />
      <label
        class="label"
        for
      >Enter zid:</label>
      <!-- TODO: sanitise input, using quotes does not work -->
      <InputZID
        v-model="zID"
        :z-i-d="zID"
      />
      <button
        class="btn btn-primary"
        type="submit"
      >
        Make admin
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import FormMessage from "@/components/FormMessage.vue";
import InputZID from "@/components/input/InputZID.vue";
// import FormError from "@/components/FormError.vue";

export default {
  name: "EventSignEnterCode",
  components: {
    //FormError,
    InputZID,
    FormMessage
  },
  props:{
    socID: {
      type: String,
      required: true
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
      axios.post('/api/society/admin', {
        zID: this.zID,
        societyID: this.socID,
        rank: 1
      }) .then(r => {
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
