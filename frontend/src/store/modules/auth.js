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
    auth_success(state, token, user){
        state.status = 'success'
        state.token = token
        state.user = user
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
                console.log(r)
                const token = r.data.token
                const user = r.data.user
                localStorage.setItem('token', token)
                commit('auth_success', token, user)
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
//   async initAuth({ state, commit, dispatch }) {
//     if (state.token) {
//       try {
//         const response = await fetchAPI("/api/auth/validate", "POST");
//         // FIXME: backend returns 'true', this is possibly bad for future.
//         if (response.data.valid === "true") {
//           // Now that we now the token is valid we can authenticate the user and validate them.
//           // However, we only want to do this if they aren't already authenticated. This is to prevent many requests from going out unnecessarily.
//           if (state.token) {
//             await dispatch('authenticateUser', state.token);
//           }
//         }
//       } catch (error) {
//         commit('resetState')
//       }
//     }
//     commit('setIsLoading', false);
//   },
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