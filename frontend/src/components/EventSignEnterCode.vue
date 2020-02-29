<template>
  <div>
    <div id="form-container--entercode" class="form-container">
      <form class="form" @submit.prevent="submitEventCodeForm">
        <h2>Sign event attendance</h2>
        <FormError v-show="formErrorMessage" :msg="formErrorMessage" />
        <div class="label-input-div">
          <label class="label" for>Event code</label>
          <!-- TODO: sanitise input, using quotes does not work -->
          <input class="input" v-model="eid" type="text" required />
        </div>
        <button class="btn btn-primary" type="submit">Next</button>
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
  data() {
    return {
      eid: "",
      formErrorMessage: "",
      allEventID: []
    };
  },
  created() {
    fetchAPI("/api/event/getAllEventID")
    .then(j => {
      this.allEventID = j
    })
  },
  methods: {
    submitEventCodeForm() {
      if (this.allEventID.includes(this.eid)) {
        this.$router.push({ name: "eventSign", params: { eid: this.eid } });
      } else {
        this.formErrorMessage = "Looks like we couldn't find that event."
      }
    }
  }
};
</script>

<style scoped>
#form-container--entercode {
  margin-top: 3rem;
}
</style>