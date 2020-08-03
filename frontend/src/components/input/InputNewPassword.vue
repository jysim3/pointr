<template>
  <div class="form-group d-flex flex-wrap w-100">
    <Input
      label="Password"
      type="password" 
      required
      :value="value"
      :valid="isPasswordValid"
      name="password" 
      error-message="Password must be between 8 to 256 characters"
      @input="$emit('input',$event)"
    />
    <Input
      v-model="repeatPassword"
      label="Repeat Password" 
      type="password"
      required
      :valid="passwordEqual"
      name="repeatPassword" 
      error-message="Your password and confirmation password do not match."
      @input="checkPassword"
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
  },
  methods: {
    checkPassword() {
      
    }   
  }
};
</script>

<style>
</style>