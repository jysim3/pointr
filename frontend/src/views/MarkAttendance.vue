<template>
  <div>
    <Logo />
    <form class="form" @submit.prevent="submitAttendanceForm">
      <div class="label-input-div">
        <label class="label" for>Event code</label>
        <input class="input" v-model="eid" type="text" required/>
      </div>
      <!-- <div class="label-input-div">
        <label class="label" for>zID</label>
        <input class="input" type="text" />
      </div>
      <div class="label-input-div">
        <label class="label" for>Name</label>
        <input class="input" type="text" />
      </div> -->
      <button class="btn btn-primary" type="submit">Go to event</button>
    </form>
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
      zid: "",
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