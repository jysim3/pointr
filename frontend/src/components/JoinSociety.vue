<template>
  <div class="form-container" id="join-society-form-container">
    <form @submit.prevent="submitJoinSocietyForm" class="form">
      <h2>Join a society</h2>
      <div class="label-input-div">
        <label for="society" class="label">Choose a society</label>
        <!-- TODO: This would need to become searchable in the future.  -->
        <select class="input--select" name="society-select">
          <option
            v-for="(society, index) in societies"
            :key="index"
            :value="society.societyName"
          >{{ society.societyName }}</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Join</button>
    </form>
  </div>
</template>

<script>
import { fetchAPI } from "@/util.js";

export default {
  name: "JoinSociety",
  data() {
    return {
      societies: [],
    };
  },
  created() {
    fetchAPI("/api/soc/getAllSocs", "GET")
      .then(j => {
        this.societies = j;
      })
      .catch(e => alert(e));
  },
  methods: {
    submitJoinSocietyForm() {
      fetchAPI("/api/soc/joinSoc", "POST", {}).catch(e => alert(e)); //TODO: need to properly handle errors in forms
      console.log(this.selected) //eslint-disable-line
    }
  }
};
</script>

<style>
</style>