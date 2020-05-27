<template>
    <div class="loader-wrap">
      <div class="loader"></div>

    </div>
</template>
<script>
export default {
    name: 'loader'
}
</script>
<style scoped>
.loader-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
}
.loader {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.loader:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #fff;
  border-color: var(--c-primary) transparent var(--c-primary) transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

</style>