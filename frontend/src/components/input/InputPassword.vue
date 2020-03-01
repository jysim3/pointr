<template>
  <div>
    <!-- Label prop should never change and hence can only be rendered once. -->
    <label v-if="label" class="label" v-once>{{ label }}</label>
    <label v-else class="label">Password</label>
    <input
      class="input"
      :class="{ 'input--invalid': !isPasswordValid }" 
      :value="password"
      @input="$emit('input', $event.target.value)"
      type="password"
      required
    />
  </div>
</template>

<script>
export default {
  name: "InputPassword",
  props: {
    label: {
      type: String,
      required: false
    },
    password: {
      type: String,
      required: true
    }
  },
  computed: {
    isPasswordValid() {
      // If nothing in input then don't make it invalid
      if (this.password.length === 0) {
        return true;
      }
      // Current requirements is at least 8 characters. Must be less than 256 characters.
      if (this.password.legnth < 8 || this.password.length > 256) {
        return false;
      }

      return true;
    }
  }
};
</script>

<style>
</style>