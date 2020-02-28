<template>
  <div class="form-container" id="join-society-form-container">
    <form @submit.prevent="submitJoinSocietyForm" class="form">
      <h2>Join a society</h2>
        <label for="society" class="label">Choose a society</label>
        <!-- TODO: This would need to become searchable in the future.  -->
        <select v-model="selectedSociety" class="input--select" name="society-select">
          <option
            v-for="(society, index) in allSocieties"
            :key="index"
            :value="society.societyName"
          >{{ society.societyName }}</option>
        </select>
      <button type="submit" class="btn btn-primary">Join</button>
    </form>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";
import auth from "@/mixins/auth";

export default {
  name: "SocietyJoin",
  mixins: [auth],
  data() {
    return {
      selectedSociety: "",
      allSocieties: [],
      success: false
    };
  },
  created() {
    fetchAPI("/api/soc/getAllSocs", "GET")
      .then(j => {
        this.allSocieties = j;
      })
      .catch(e => console.log(e)); //eslint-disable-line
  },
  methods: {
    submitJoinSocietyForm() {
      fetchAPI(`/api/soc/join`, "POST", {
        zID: this.getZID(),
        socID: this.selectedSociety.soceityID
      })
      .then(r => {
        if (r.status === 200) {
          this.success = true
        }
      })
      .catch(e => alert(e));
    }
  }
};
</script>

<style>
</style>