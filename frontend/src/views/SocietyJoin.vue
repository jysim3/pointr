<template>
  <div class="form-container" id="join-society-form-container">
    <form @submit.prevent="submitJoinSocietyForm" class="form">
      <h2>Join a society</h2>
        <FormError v-if="error.status" :msg="error.msg" />
        <label for="society" class="label">Choose a society</label>
        <!-- TODO: This would need to become searchable in the future.  -->
        <select v-model="selectedSociety" class="input--select" name="society-select">
          <option
            v-for="(society, index) in allSocieties"
            :key="index"
            :value="society"
          >{{ society.societyName }}</option>
        </select>
      <button type="submit" class="btn btn-primary">Join</button>
    </form>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import auth from "@/mixins/auth";
import FormError from "@/components/FormError.vue";

export default {
  name: "SocietyJoin",
  mixins: [auth],
  components: {
    FormError
  },
  data() {
    return {
      selectedSociety: "",
      allSocieties: [],
      success: false,
      error: {
        status: false,
        msg: ""
      }
    };
  },
  async created() {
    const response = await fetchAPI("/api/soc/getAllSocs")
    // TODO: allSocieties should only contain ones user has not alreaedy joined, this data should be in the vuex store.
    this.allSocieties = response.data;
  },
  methods: {
    submitJoinSocietyForm() {
      fetchAPI(`/api/soc/join`, "POST", {
        societyID: this.selectedSociety.societyID
      })
      .then(r => {
        if (r.status === 200) {
          this.success = true
        } else if (r.status === 403) {
          this.error.status = true;
          this.error.msg = false;
        } else {
          this.error.status = true;
          this.error.msg = `There was an error while trying to join ${this.selectedSociety.societyName}`;
        }
      })
      .catch(e => console.log(e)); //eslint-disable-line
    }
  }
};
</script>

<style>
</style>