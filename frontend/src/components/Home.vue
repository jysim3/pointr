<template>
  <div id="home-container">
    <div class="center">
      <h1 class="title">Room Pointer</h1>
      <form @submit="submitForm"> 
        <input v-model="eid" type="text" />
      </form> 
    </div>
  </div>
</template>

<script>
import router from '@/router/index.js'
export default {
  name: 'Home',
  data() {
    return {
      eid: ''
    }
  },
  props: {
    msg: String
  },
  methods: {
    submitForm() {
      router.push({name: "event", params: {eid: this.eid}})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "../assets/style.css";

#home-container {
  background-color: var(--primary-yellow);
  margin: 0;
  width: 100vw;
  height: 100vh;
}

.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width:100%;
}
</style>
