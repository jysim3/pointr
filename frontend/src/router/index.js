import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store/index';
import Home from '@/views/Home.vue';
import EventSign from '@/views/EventSign-DEPRECATE.vue';
import UserProfile from '@/views/UserProfile.vue';
import RequestForm from '@/views/RequestForm.vue'

Vue.use(VueRouter);
import eventRoutes from './event'
import authRoutes from './auth'
import societyRoutes from './society'

const DEFAULT_TITLE = "Pointr"
const routes = [
  ...authRoutes,
  ...eventRoutes,
  ...societyRoutes,
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
        title: 'Home - Pointr'
    }
  },
  {
    path: '/request',
    name: 'request',
    component: RequestForm,
    props: true,
    meta: {
        title: 'Contact - Pointr'
    }
  },
  {
    path: '/sign/:eventID?',
    name: 'eventSign',
    component: EventSign,
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {

    path: '/user/:zID?',
    name: 'userProfile',
    component: UserProfile,
    props: true,
    meta: {
      requiresAuth: true
    }
  }
];

const router = new VueRouter({
  mode: 'history',
  routes
});

// For more info regarding this visit:
// https://scotch.io/tutorials/handling-authentication-in-vue-using-vuex
router.beforeResolve(async (to, from, next) => {
  // EXAMPLE: user with no account scans QR code on Event page

  store.dispatch('auth/validate')
  if (store.getters.isAuthenticated) {
    if (store.getters['user/status'] === null) {
      await store.dispatch('user/getUserInfo')
    }
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isAuthenticated) {
      next({
        path: '/signin',
        query: {redirect: to.fullPath}, 
      });
      return 
    }
  }
  next();
});


router.beforeEach((to, from, next) => {
  document.title = to.meta && to.meta.title || DEFAULT_TITLE
  next()
})

export default router;
export { routes }