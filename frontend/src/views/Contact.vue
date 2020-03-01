<template>
  <div>
  <div class="card-container">
    <div class="card">
      <h2>You can contact us via email at</h2>
      <h1>{{ this.email }}</h1>
      <a id="email-link" :href="`mailto:${this.email}`">Open an email to us.</a>
    </div>
  </div>
  </div>
</template>

<script>
export default {
  name: "Contact",
  data() {
    return {
      email: "pointr.help@gmail.com"
    };
  }
};
</script>

<style scoped>
.card {
    width: 50%;
}

#email-link {
    margin-top: 2rem;
    font-size: 1.5rem;
}
</style>