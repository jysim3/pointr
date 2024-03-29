import Vue from 'vue'
import App from './App.vue'
import router from '@/router/index'
import store from '@/store/index'
import axios from 'axios'

Vue.config.productionTip = false
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = token
}
if (process.env.NODE_ENV === 'development'){
  axios.defaults.baseURL = 'http://localhost:5000'
} else if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = 'https://pointr.live';
} else {
  axios.defaults.baseURL = 'http://api:5000'
}
axios.interceptors.response.use(undefined, function (err) {
  return new Promise(function () {
    if (err.response && err.response.status === 401) {
      store.dispatch('logout')
    }
    throw err
  })
})


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

export const apiURL = 'localhost:5000/'
