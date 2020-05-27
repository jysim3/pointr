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
axios.defaults.baseURL = 'http://localhost:5000'


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

export const apiURL = 'localhost:5000/'
