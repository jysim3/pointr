import Vue from 'vue';
import Vuex from 'vuex';
import user from './modules/user';
import auth from './modules/auth';
import jwt from "jsonwebtoken";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    status: 'success',
    navBar: true
  },
  mutations: {
    loading: (state, status) => status ? state.status = 'loading' : state.status = 'success',
    navBar: (state, navBar) => state.navBar = navBar
  },
  getters: {
    isAuthenticated: (state) => !!state.auth.token,
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
      return new Promise(async (resolve,reject) => {
        try {
          await dispatch('auth/logout')
          commit('user/clearUserInfo')
          resolve()
        } catch (error) {
          console.log(error); //eslint-disable-line
          console.log(error.response); //eslint-disable-line
          reject()
        }
      })
    }
  },
  modules: {
    user,
    auth
  }
});

export default store;
