<template>
  <Input
    label="zID"
    type="text" 
    :value="value"
    :valid="isZIDValid"
    error-message="Invalid zID" 
    name="zID"
    @input="$emit('input', $event)"
  />
</template>

<script>
import Input from '@/components/input/Input.vue'
export default {
  name: "InputZID",
  components: {
    Input
  },
  props: {
    value: {
      type: String,
    },
  },
  computed: {
    isZIDValid() {
      // Eg z5267516 or 5267516 will both work.
      // If nothing in input then don't make it invalid
      return this.value.length === 0 || /^[zZ]?[0-9]{7}$/.test(this.value);
    }
  }
};
</script>

<style>
</style>