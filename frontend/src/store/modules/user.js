import { fetchAPI } from '@/util';

// Currently the validity of a user's token will only be checked once,
// this is to prevent a lot of requests to the backend.

const state = {
  authToken: localStorage.getItem('authToken') || '',
  isAuthenticated: false,
  isAdmin: false,
  info: {
    zID: '',
    name: '',
    societies: {
      member: [],
      staff: []
    }
    // TODO: make sure everything that will be mutated is already here.
  }
};

const getters = {
  memberSocieties(state) {
    return state.info.societies.member;
  },
  staffSocieties(state) {
    return state.info.societies.staff;
  },
  allSocieties(state, getters) {
    return [...getters.memberSocieties, ...getters.staffSocieties];
  },
  isSocietyAdmin(state) {
    return state.info.societies.staff.length > 0;
  },
  allEvents() {
    return;
  }
};

const mutations = {
  authToken(state, authToken) {
    localStorage.setItem('authToken', authToken);
    state.authToken = authToken;
  },
  info(state, info) {
    state.info = info;
  },
  resetState(state) {
    localStorage.removeItem('authToken');
    state.authToken = '';
    state.isAuthenticated = false;
    state.isAdmin = false;
    state.info = {};
  },
  setIsAdmin(state, adminState) {
    state.isAdmin = adminState;
  },
  setIsAuthenticated(state) {
    state.isAuthenticated = true;
  }
};

const actions = {
  async authenticateUser({ dispatch, commit }, authToken) {
    // Currently, this action should only be called if we know that the token is valid.
    commit('authToken', authToken);
    await dispatch('userInfo');
    commit('setIsAuthenticated');
    commit('setIsAdmin', getters.isSocietyAdmin);
  },
  async userInfo({ commit }) {
    try {
      const routes = [
        '/api/user/info',
        '/api/user/involvedSocs',
        '/api/user/permission'
      ];
      const [
        infoResponse,
        involvedSocsResponse,
        permissionResponse
      ] = await Promise.all(routes.map(route => fetchAPI(route)));

      commit('info', {
        ...infoResponse.data,
        societies: involvedSocsResponse.data,
        permission: permissionResponse.data.permission
      });
    } catch (error) {
      console.log(error); //eslint-disable-line
    }
  },
  signOut({ commit }) {
    commit('resetState');
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
