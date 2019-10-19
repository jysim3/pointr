<template>
  <div id="app">
    <SignIn/>
  </div>
</template>

<script>
import SignIn from './components/SignIn.vue'
export const apiURL = 'localhost:5000'

export default {
  name: 'app',
  components: {
    SignIn
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto:400,100,400i,700i,700');
html{
  font: 100%/1.5 "Roboto", Verdana, sans-serif;
}
h1, .alpha {
    margin-bottom: 1.5rem;
    font-size: 6rem;
    font-weight: 100;
    line-height: 1;
    letter-spacing: -.05em;
}
.title{
    color: #f35626;
    background-image: linear-gradient(92deg, #f35626 0%,#feab3a 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: hue 60s infinite linear;
}
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
