<template>
  <div>
    <Input label="Password" type="password" 
    :value="value"
    @input="$emit('input',$event)"
    :valid="isPasswordValid" 
    errorMessage="Password must be between 8 to 256 characters"
    />
    <Input label="Repeat Password" type="password" 
    v-model="repeatPassword"
    @input="checkPassword"
    :valid="passwordEqual" 
    errorMessage="Your password and confirmation password do not match."
    />
  </div>
</template>

<script>
import Input from '@/components/input/Input.vue'
export default {
  name: "InputPassword",
  components: {
    Input
  },
  props: {
    label: {
      type: String,
      required: false
    },
    value: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      repeatPassword: ""
    }
  },
  methods: {
    checkPassword() {
      
    }   
  },
  computed: {
    passwordEqual() {
      return this.repeatPassword.length === 0 || this.repeatPassword === this.value
      
    },
    isPasswordValid() {
      // If nothing in input then don't make it invalid
      if (this.value.length === 0) {
        return true;
      }
      // Current requirements is at least 8 characters. Must be less than 256 characters.
      if (
        this.value.length < 8 || 
        this.value.length > 256 ) {
        return false;
      }

      return true;
    }
  }
};
</script>

<style>
</style>