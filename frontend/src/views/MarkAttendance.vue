<template>
  <div>
    <Logo />
    <div class="form-container">
      <form class="form" @submit.prevent="submitAttendanceForm">
        <div class="label-input-div">
          <label class="label" for>Event code</label>
          <input class="input" v-model="eid" type="text" required />
        </div>
        <button class="btn btn-primary" type="submit">Go to event</button>
      </form>
    </div>
  </div>
</template>

<script>
import router from "@/router/index.js";
import Logo from "@/components/Logo.vue";

export default {
  name: "MarkAttendance",
  components: {
    Logo
  },
  data() {
    return {
      eid: "",
      zID: "",
      name: ""
    };
  },
  methods: {
    submitAttendanceForm() {
      router.push({ name: "signEvent", params: { eid: this.eid } });
    }
  }
};
</script>

<style>
</style>