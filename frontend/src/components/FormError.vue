<template>
  <p class="form-error-msg">{{ msg }}</p>
</template>

<script>
export default {
  name: "FormError",
  props: {
    msg: String
  }
};
</script>