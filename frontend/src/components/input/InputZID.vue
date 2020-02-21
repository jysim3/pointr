<template>
  <div class="label-input-div">
    <label class="label">zID</label>
    <input
      class="input"
      :class="{ 'input--invalid': !isZIDValid }"
      :value="zID"
      @input="$emit('input', $event.target.value)"
      type="text"
      required
    />
  </div>
</template>

<script>
export default {
  name: "InputZID",
  props: {
    zID: {
      type: String,
      required: true
    }
  },
  computed: {
    isZIDValid() {
      // Eg z5267516 or 5267516 will both work.
      // If nothing in input then don't make it invalid
      if (this.zID.length === 0) {
        return true;
      }
      const re = RegExp("^[zZ]?[0-9]{7}$");
      return re.test(this.zID);
    }
  }
};
</script>

<style>
</style>