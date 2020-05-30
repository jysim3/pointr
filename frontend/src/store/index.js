import Vue from 'vue';
import Vuex from 'vuex';
import user from './modules/user';
import auth from './modules/auth';
import jwt from "jsonwebtoken";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    status: 'success'
  },
  mutations: {
    loading: (state, status) => status ? state.status = 'loading' : state.status = 'success',
  },
  getters: {
    isAuthenticated: state => !!state.auth.token,
    isLoading: state => state.status === 'loading',
    zID: state => state.auth.token ? jwt.decode(state.auth.token)['zID'] : ''
  },
  actions: {
    login({dispatch}, loginDetails) {
      return dispatch('auth/login', loginDetails)
        .then(() => dispatch('user/getUserInfo'))
        .catch(error => {
          console.log(error); //eslint-disable-line
          console.log(error.response); //eslint-disable-line
        })
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
