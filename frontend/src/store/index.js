import Vue from 'vue';
import Vuex from 'vuex';
import user from './modules/user';
import auth from './modules/auth';

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
    isLoading: state => state.status === 'loading'
  },
  modules: {
    user,
    auth
  }
});

export default store;
