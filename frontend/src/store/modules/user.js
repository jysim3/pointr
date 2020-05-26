// import { fetchAPI } from '@/util';
import axios from 'axios';

// TODO: make user.js about user information, make auth.js for authentication purposes
// Currently the validity of a user's token will only be checked once,
// this is to prevent a lot of requests to the backend.

const state = {
  status: null,
  zID: "",
  firstName: "",
  lastName: "",
  attendedEvents: [],
  events: [],
  societies: {
    member: [],
    staff: []
  },
  permission: 0
};

const getters = {
  name: (state) => `${state.firstName} ${state.lastName}`,
  zID: (state) => state.zID,
  status: state => state.status,
  memberSocieties(state) {
    if (state.societies) {
      return state.societies.member;
    } else {
      return []
    }
  },
  staffSocieties(state) {
    if (state.societies) {
      return state.societies.staff;
    } else {
      return []
    }
  },
  joinedSocieties(state) {
    if (state.societies) {
      return state.societies.member.concat(state.societies.staff);
    } else {
      return []
    }
  },
  isSocietyAdmin: (state) => socID => {
    console.log(socID) // eslint-disable-line
    console.log(state.societies.staff) // eslint-disable-line
    return state.societies.staff.some(v => v.societyID === socID)
  },
  // https://vuex.vuejs.org/guide/getters.html#method-style-access
  allSocietyEvents: (state) => socIDs => {
    return state.events.filter(v => v.societyID.includes(socIDs))
  },
  event: (state) => eventID => {
    return state.events.find(v => v.eventID === eventID)
  },
  allEvents: (state) => state.events,
  staffEvents(state, getters) {
    const staffSocIDs = state.societies.staff.reduce((a, society) => a.concat(society.societyID), [])
    return getters.allSocietyEvents(state, staffSocIDs)
  },

};

const mutations = {
  userInfo(state, userInfo) {
    state.description = userInfo.description
    state.events = userInfo.events
    state.firstName = userInfo.firstName
    state.image = userInfo.image
    state.lastName = userInfo.lastName
    state.societies = userInfo.societies
    state.zID = userInfo.zID
  },
  eventInfo(state, eventInfo) {
    state.events = eventInfo
  },
};

const actions = {
  async authenticateUser({ dispatch, commit }, authToken) {
    // Currently, this action should only be called if we know that the token is valid.
    commit('authToken', authToken);
    await dispatch('userInfo');
    commit('setIsAdmin');
  },
  async getUserInfo({ commit }) {
    try {
      const requests = [
        {
          url: '/api/user/',
          method: 'GET'
        },
        {
          url: '/api/user/getUpcomingEvents',
          method: 'GET'
        }
      ];
      const [
        infoResponse,
        eventResponse
      ] = await Promise.all(requests.map(r => axios(r)))
      commit('userInfo', infoResponse.data)
      commit('eventInfo', eventResponse.data)
    } catch (error) {
      console.log(error); //eslint-disable-line
      console.log(error.response); //eslint-disable-line
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
