import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import CreateEvent from '../views/CreateEvent.vue'
import Event from '../views/Event.vue'
import SignEvent from '../views/SignEvent.vue'
import User from '../views/User.vue'
import MarkAttendance from '../views/MarkAttendance.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/mark-attendance',
    name: 'markAttendance',
    component: MarkAttendance
  },
  {
    path: '/create',
    name: 'create',
    component: CreateEvent
  },
  {
    path: '/u/:zid',
    name: 'user',
    component: User,
    props: true
  },
  {
    path: '/event/:eid',
    name: 'event',
    component: Event,
    props: true
  },
  {
    path: '/e/:eid',
    name: 'signEvent',
    component: SignEvent,
    props: true
  }
]

const router = new VueRouter({
  routes
})

export default router
