import axios from 'axios'
import jwt from "jsonwebtoken";
import router from '@/router/index';
const state = {
  token: localStorage.getItem('token') || '',
}
const getters = {
  isAuthenticated:state => !!state.token
}
const mutations = {

  auth_request(state){
    state.status = 'loading'
  },
  auth_success(state, token){
    state.status = 'success'
    state.token = token
    axios.defaults.headers.common['Authorization'] = token
  },
  auth_error(state){
    state.status = 'error'
  },
  resetState(state){
    state.status = '',
    state.token = ''
  },
}
const actions = {
  validate(){ 
    return

  },
  register({commit}, user){
    return new Promise((resolve, reject) => {
      commit('auth_request')
      axios({url: '/api/auth/register', data: user, method: 'POST' })
        .then(resp => {
          // const token = resp.data.token
          // const user = resp.data.user
          // localStorage.setItem('token', token)
          // axios.defaults.headers.common['Authorization'] = token
          // commit('auth_success', token, user)
          resolve(resp)
        })
        .catch(err => {
          commit('auth_error', err)
          localStorage.removeItem('token')
          reject(err)
        })
    })
  },
  login({commit}, loginDetails) {
    return new Promise((resolve, reject) => {
      commit('auth_request')
      axios({
        url: '/api/auth/login',
        data: loginDetails,
        method: 'POST'
      })
        .then(r => {
          const token = r.data.data.token
          const decodedToken = jwt.decode(token)
          if (decodedToken['permission'] === 0) {
            router.push({
              name: 'sendActivationEmail', 
              params: {givenzID: decodedToken['zID']}
            })
            reject(r)
            return r
          }
          localStorage.setItem('token', token)
          commit('auth_success', token)
          resolve(r)
        })
        .catch(e => {
          commit('auth_error')
          localStorage.removeItem('token')
          console.log('fail')
          reject(e)
        })

    })
  },
  logout({ commit }) {
    return new Promise((resolve) => {
      commit('resetState')
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
      resolve()
    })
  }
}
export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};