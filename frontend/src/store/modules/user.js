import { fetchAPI } from '@/util';

// Currently the validity of a user's token will only be checked once,
// this is to prevent a lot of requests to the backend.

const state = {
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
  isAuthenticated: () => state.isAuthenticated,
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
  joinedSocieties(state) {
    if (state.info.societies) {
      return state.info.societies.member.concat(state.info.societies.staff);
    } else {
      return []
    }
  },
  isSocietyAdmin: (state) => socID => {
    console.log(socID) // eslint-disable-line
    console.log(state.info.societies.staff) // eslint-disable-line
    return state.info.societies.staff.some(v => v.societyID === socID)
  },
  // https://vuex.vuejs.org/guide/getters.html#method-style-access
  allSocietyEvents: (state) => socIDs => {
      return state.info.events.filter(v => v.societyID.includes(socIDs))
  },
  event: (state) => eventID => {
      return state.info.events.find(v => v.eventID === eventID)
  },
  allEvents: (state) => state.info.events,
  staffEvents (state, getters) {
    const staffSocIDs = state.info.societies.staff.reduce((a, society) => a.concat(society.societyID), [])
    return getters.allSocietyEvents(state,staffSocIDs)
  },

};

const mutations = {
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
    state.isAuthenticated = false
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
  setIsLoading(state, isLoading) {
    state.isLoading = isLoading;
  },
  authenticateUser(state) {
    state.isAuthenticated = true
  }
};

const actions = {
  async userInfo({ commit }) {
    try {
      const requests = [
        {
          url: '/api/user/',
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
        permissionResponse,
        eventResponse
      ] = await Promise.all(requests.map(r => fetchAPI(r.url, r.method)));
      const events = eventResponse.data

      // TODO: this is messy, should rather be defining in initial state or backend should not be returning undefined


      console.log(infoResponse.data) //eslint-disable-line
      console.log(permissionResponse.data) //eslint-disable-line
      console.log(events) //eslint-disable-line
      const infoPayload = {
        ...infoResponse.data,
        ...permissionResponse.data,
        events,
      }
        
       
      commit('info', infoPayload);
      console.log(infoPayload) //eslint-disable-line
    } catch (error) {
      console.log(error); //eslint-disable-line
      console.log(error.response); //eslint-disable-line
    }
  },
  async initAuth({ commit, dispatch }) {
    try {
      const response = await fetchAPI("/api/auth/validate", "POST");
      if (response.data.valid === "true") {
        // Now that we now the token is valid we can authenticate the user and validate them.
        // However, we only want to do this if they aren't already authenticated. This is to prevent many requests from going out unnecessarily.
        if (!state.isAuthenticated) {
          await commit('authenticateUser');
          await dispatch('userInfo');
          await commit('setIsAdmin');
        }
      }
    } catch (error) {
      console.log(error.response) //eslint-disable-line
    }
    commit('setIsLoading', false);
  },
  signOut({ commit }) {
    fetchAPI('/api/auth/logout', 'POST')
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
