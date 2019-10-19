<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>


<script>
export const apiURL = 'http://localhost:5000'

export default {
  name: 'app',
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
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
