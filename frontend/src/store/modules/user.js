// import { fetchAPI } from '@/util';
import axios from 'axios';

// TODO: make user.js about user information, make auth.js for authentication purposes
// Currently the validity of a user's token will only be checked once,
// this is to prevent a lot of requests to the backend.

const getDefaultState = () => {
    return {
    attended: [],
    status: null,
    commencementyear: null,
    degree: null,
    description: null,
    faculty: null,
    firstname: "",
    interested: [],
    isarc: false,
    lastname: "",
    photo: null,
    preferredName: "",
    school: null,
    zID: "",
    societies: {
      member: [],
      staff: []
    },
  }
};
const state = getDefaultState()

const getters = {
  name: (state) => `${state.firstname} ${state.lastname}`,
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
  isSocietyAdmin: (state) => socID => {
    return state.societies.staff.some(v => v.societyID === socID)
  },

};

const mutations = {
  userInfo(state, userInfo) {

    state.attended = userInfo.attended
    state.commencementyear = userInfo.commencementyear
    state.degree = userInfo.degree
    state.description = userInfo.description
    state.faculty = userInfo.faculty
    state.firstname = userInfo.firstname
    state.interested = userInfo.interested
    state.isarc = userInfo.isarc
    state.lastname = userInfo.lastname
    state.photo = userInfo.photo
    state.preferredName = userInfo.preferredName
    state.school = userInfo.school
    state.zID = userInfo.zID
    state.status = 'success'
  },
  societyInfo(state, societyInfo) {
    console.log(societyInfo)
  },
  eventInfo(state, eventInfo) {
    state.events = eventInfo
  },
  clearUserInfo(state) {
    Object.assign(state, getDefaultState())
  }
};

const actions = {
  async authenticateUser({ dispatch, commit }, authToken) {
    // Currently, this action should only be called if we know that the token is valid.
    commit('authToken', authToken);
    await dispatch('userInfo');
    commit('setIsAdmin');
  },
  async getUserInfo({ commit, rootGetters }) {
    try {
      console.log(rootGetters.zID)
      const requests = [
        {
          url: '/api/user',
          params: {
            zID: rootGetters.zID
          },
          method: 'GET'
        },
        {
          url: '/api/user/events/upcoming',
          method: 'GET'
        },
        {
          url:  'api/user/societies',
          method: 'GET'
        }
      ];
      console.log('hihi')
      const [
        infoResponse,
        eventResponse,
        societyResponse
      ] = await Promise.all(requests.map(r => axios(r)))
      console.log(infoResponse.data)
      commit('userInfo', infoResponse.data.data)
      commit('societyInfo', societyResponse.data.data)
      commit('eventInfo', eventResponse.data.data)
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
