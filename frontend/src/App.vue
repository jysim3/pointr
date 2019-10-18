<template>
  <div id="app">
    <SignIn/>
    <Home/>
  </div>
</template>

<script>
import Home from './components/Home.vue'
import SignIn from './components/SignIn.vue'

export default {
  name: 'app',
  components: {
    Home,
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
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
