import axios from 'axios'
const state = {
  token: localStorage.getItem('token') || '',
}
const getters = {
//   isAuthenticated: state => !!state.token,
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
    login({commit}, loginDetails) {
        return new Promise((resolve, reject) => {
            commit('auth_request')
            commit('loading', true, { root: true})
            axios({
                url: '/api/auth/login',
                data: loginDetails,
                method: 'POST'
            })
            .then( r => {
                const token = r.data.data.token
                localStorage.setItem('token', token)
                commit('auth_success', token)
                resolve(r)
            })
            .catch(e => {
                commit('auth_error')
                localStorage.removeItem('token')
                reject(e)
            }).finally(() => {
                commit('loading', false, { root: true})
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