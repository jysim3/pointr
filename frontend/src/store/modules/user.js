import { fetchAPI } from '@/util';

// Currently the validity of a user's token will only be checked once,
// this is to prevent a lot of requests to the backend.

const state = {
  authToken: localStorage.getItem('authToken') || '',
  isAuthenticated: false,
  isAdmin: false,
  info: {
    zID: "",
    name: "",
    attendedEvents: [],
    events: [],
    societies: {
      member: [],
      staff: []
    },
    permission: 0
  },
  // info: {},
    // TODO: make sure everything that will be mutated is already here.
  isLoading: true //TODO: move this into a global store
};

const getters = {
  memberSocieties(state) {
    if (state.info.societies) {
      return state.info.societies.member;
    } else {
      return []
    }
  },
  staffSocieties(state) {
    if (state.info.societies) {
      return state.info.societies.staff;
    } else {
      return []
    }
  },
  allSocieties(state) {
    if (state.info.societies) {
      return state.info.societies.member.concat(state.info.societies.staff);
    } else {
      return []
    }
  },
  // https://vuex.vuejs.org/guide/getters.html#method-style-access
  allEvents: (state) => socIDs => {
    if (socIDs){
      return state.info.events.filter(v => v.societyID.includes(socIDs))
    }
    return state.info.events;
  },
  staffEvents (state, getters) {
    const staffSocIDs = state.info.societies.staff.reduce((a, society) => a.concat(society.societyID), [])
    return getters.allEvents(state,staffSocIDs)
  },

};

const mutations = {
  authToken(state, authToken) {
    localStorage.setItem('authToken', authToken);
    state.authToken = authToken;
  },
  info(state, infoPayload) {
    // state.info.zID = info.zID,
    // state.info.name = info.name,
    // state.info.events = info.events,
    // state.info.societies.member = info.societies.member,
    // state.info.societies.staff = info.societies.staff
    // state.info.permission = info.permission
    state.info = { ...infoPayload }
  },
  resetState(state) {
    localStorage.removeItem('authToken');
    state.authToken = '';
    state.isAuthenticated = false;
    state.isAdmin = false;
    state.info = {};
  },
  setIsAdmin(state) {
    if (state.info.societies.staff.length > 0) {
      state.isAdmin = true;
    } else {
      state.isAdmin = false;
    }
  },
  setIsAuthenticated(state) {
    state.isAuthenticated = true;
  },
  setIsLoading(state, isLoading) {
    state.isLoading = isLoading;
  }
};

const actions = {
  async authenticateUser({ dispatch, commit }, authToken) {
    // Currently, this action should only be called if we know that the token is valid.
    commit('authToken', authToken);
    commit('setIsAuthenticated');
    await dispatch('userInfo');
    commit('setIsAdmin');
  },
  async userInfo({ commit }) {
    try {
      const requests = [
        {
          url: '/api/user/info',
          method: 'POST'
        },
        {
          url: '/api/user/involvedSocs',
          method: 'GET'
        },
        {
          url: '/api/auth/permission',
          method: 'POST'
        },
        {
          url: '/api/user/getUpcomingEvents',
          method: 'GET'
        }
      ];
      const [
        infoResponse,
        involvedSocsResponse,
        permissionResponse,
        eventResponse
      ] = await Promise.all(requests.map(r => fetchAPI(r.url, r.method)));
      const events = eventResponse.data

      // TODO: this is messy, should rather be defining in initial state or backend should not be returning undefined
      let societies;
      if (!involvedSocsResponse.data) {
        societies = {
          member: [],
          staff: []
        }
      } else {
        societies = {
          member: involvedSocsResponse.data.member,
          staff: involvedSocsResponse.data.staff
        }

      }


      const infoPayload = {
        ...infoResponse.data,
        ...permissionResponse.data,
        events,
        societies,
      }
      commit('info', infoPayload);
      console.log(infoPayload) //eslint-disable-line
    } catch (error) {
      console.log(error); //eslint-disable-line
      console.log(error.response); //eslint-disable-line
    }
  },
  async initAuth({ state, commit, dispatch }) {
    if (state.authToken) {
      try {
        const response = await fetchAPI("/api/auth/validate", "POST");
        // FIXME: backend returns 'true', this is possibly bad for future.
        if (response.data.valid === "true") {
          // Now that we now the token is valid we can authenticate the user and validate them.
          // However, we only want to do this if they aren't already authenticated. This is to prevent many requests from going out unnecessarily.
          if (!state.isAuthenticated) {
            await dispatch('authenticateUser', state.authToken);
          }
        }
      } catch (error) {
        console.log(error.response) //eslint-disable-line
      }
    }
    commit('setIsLoading', false);
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
