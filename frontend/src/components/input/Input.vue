<template>
  <div>
    <label class="label">{{label}}</label>
    <input
      class="input"
      :class="{ 'input--invalid': !valid }"
      :value="value"
      @input="sendInput"
      :type="type"
      :required="required"
    />
  </div>
</template>

<script>
export default {
  name: "Input",
  props: {
      valid: {
          type: Boolean,
          default: true
      }, 
      value: {
          type: String
      }, 
      type: {
          type: String
      }, 
      label: {
          type: String
      },
      required: {
            type: Boolean,
            default: true
      },
      errorMessage: {
          type: String,
          default: "Error"
      }
  },
  methods: {
      sendInput(event) {
        this.$emit('input', event.target.value)
        this.$nextTick(() => event.target.setCustomValidity(!this.valid?this.errorMessage:''))
      }
  },
};
</script>

<style>
</style>