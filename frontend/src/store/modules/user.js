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
      members: [],
      admins: []
    },
  }
};
const state = getDefaultState()

const getters = {
  name: (state) => `${state.firstname} ${state.lastname}`,
  zID: (state) => state.zID,
  status: state => state.status,
  societies: (state) => state.societies,
  isSocietyMember: (state) => socID => {
    if (Array.isArray(socID)){
      return state.societies.members.some(v => socID.includes(v.id))
    }
    return state.societies.members.some(v => v.id === socID)
  },
  isSocietyAdmin: (state) => socID => {
    if (Array.isArray(socID)){
      return state.societies.admins.some(v => socID.includes(v.id))
    }
    return state.societies.admins.some(v => v.id === socID)
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
    Object.assign(state.societies, societyInfo)
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
  getUserInfo({ commit, rootGetters }) {
    return new Promise((resolve,reject) => {
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
        Promise.all(requests.map(r => axios(r)))
        .then(([ infoResponse, eventResponse, societyResponse]) => {
        commit('userInfo', infoResponse.data.data)
        commit('societyInfo', societyResponse.data.data)
        commit('eventInfo', eventResponse.data.data)
        resolve([ infoResponse, eventResponse, societyResponse])
      }).catch ((error) => {
        reject(error)
      })

    })
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
