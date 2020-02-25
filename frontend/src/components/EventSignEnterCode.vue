<template>
  <div>
    <div class="form-container">
      <form class="form" @submit.prevent="submitEventCodeForm">
        <h2>Sign event attendance</h2>
        <div class="label-input-div">
          <label class="label" for>Event code</label>
          <input class="input" v-model="eid" type="text" required />
        </div>
        <button class="btn btn-primary" type="submit">Next</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "EventSignEnterCode",
  data() {
    return {
      eid: "",
    };
  },
  methods: {
    submitEventCodeForm() {
      // TODO: check that this is an event before pushing
      this.$router.push({ name: "eventSign", params: { eid: this.eid } });
    }
  }
};
</script>

<style>
</style>