import Vue from 'vue';
import Vuex from 'vuex';
import user from './modules/user';
import auth from './modules/auth';
import jwt  from "jsonwebtoken";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    status: 'success',
    navBar: true,
    eventTags: ['Study', 'Party', 'Food', 'Online/Virtual']
  },
  mutations: {
    loading: (state, status) => status ? state.status = 'loading' : state.status = 'success',
    navBar: (state, navBar) => state.navBar = navBar
  },
  getters: {
    eventTags: state => state.eventTags.map((v,i)=>({value:v,id:i})),
    isAuthenticated: (state, getters) => getters['auth/isAuthenticated'],
    tokenInfo: (state) => !!state.auth.token && jwt.decode(state.auth.token),
    isLoading: state => state.status === 'loading',
    navBar: state => state.navBar,
    zID: state => state.auth.token ? jwt.decode(state.auth.token)['zID'] : '',
  },
  actions: {
    login({dispatch}, loginDetails) {
      return dispatch('auth/login', loginDetails)
        .then(() => dispatch('user/getUserInfo'))
    },
    logout({commit, dispatch}) {
      return new Promise((resolve,reject) => {
        dispatch('auth/logout')
          .then(() => commit('user/clearUserInfo'))
          .then(() => resolve())
          .catch(error => {
            console.log(error)
            reject()
          })
      })
    }
  },
  modules: {
    user,
    auth
  }
});

export default store;
