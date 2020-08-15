<template>
  <div class="event-code-display-container">
    <div class="event-code-display">
      <h4 class="header">
        Event code
      </h4>
      <h2 class="code">
        {{ eventID }}
      </h2>
    </div>
  </div>
</template>

<script>
export default {
  name: "EventCodeDispaly",
  props: {
    eventID: String
  }
};
</script>

<style scoped>
.event-code-display-container {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  color: black;
}

.event-code-display {
  background-color: white;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.05);
  display: inline-block;
  text-align: center;
  padding: 1rem 3rem;
  border-radius: var(--border-radius);
}

.event-code-display .header {
  color: var(--c-secondary-dark);
}
</style>