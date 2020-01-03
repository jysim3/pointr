import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import CreateEvent from '../views/CreateEvent.vue'
import Event from '../views/Event.vue'
import SignEvent from '../views/SignEvents.vue'
import User from '../views/User.vue'
import Statistics from '@/views/Statistics.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
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
  },
  {
    path: '/stats',
    name: 'stats',
    component: Statistics
  },
]

const router = new VueRouter({
  routes
})

export default router
