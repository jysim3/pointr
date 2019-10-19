import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import CreateEvent from '../views/CreateEvent.vue'
import Event from '../views/Event.vue'
import SignEvents from '../views/SignEvents.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/e/:eid',
    name: 'signEvents',
    component: SignEvents,
    props: true
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
    path: '/event/:eid',
    name: 'event',
    component: Event,
    props: true
  }
]

const router = new VueRouter({
  routes
})

export default router
