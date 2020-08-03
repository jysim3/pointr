<template>
  <p
    v-if="msg.success === false"
    class="form-error-msg"
  >
    {{ msg.message }}
  </p>
  <p
    v-else-if="msg.success === true"
    class="form-success-msg"
  >
    {{ msg.message }}
  </p>
</template>

<script>
export default {
  name: "FormError",
  props: {
    msg: Object
  }
};
</script>
<style scoped>

.form-success-msg {
  color: var(--c-success);
  font-weight: 500;
  text-align: center;
  font-size: 1.25rem;
  text-transform: capitalize;
}
</style>