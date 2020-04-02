import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store/index';
import Home from '@/views/Home.vue';
import EventSign from '@/views/EventSign-DEPRECATE.vue';
import Contact from '@/views/Contact.vue';

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
    // TODO: only the creator of the society/event should be able to access this, need to have function that checks they are authorized after we know they are authenticated.
  {
    path: '/contact',
    component: Contact,
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
];

const router = new VueRouter({
  mode: 'history',
  routes
});

// For more info regarding this visit:
// https://www.digitalocean.com/community/tutorials/how-to-set-up-vue-js-authentication-and-route-handling-using-vue-router
router.beforeResolve(async (to, from, next) => {
  // TODO: what if user goes sign in -> sign up from link in sign in form, then they may not end up at original, intended path
  // TODO: signed in user should not be able to go to sign in or sign up
  // EXAMPLE: user with no account scans QR code on Event page
  await store.dispatch('user/initAuth');
  
  // Prevents normal users going on prevent page etc.
  // TODO: need to decide how to handle requiresAdmin for event pages
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (!store.state.user.isAdmin) {
      next({ name: 'home' })
    } else {
      next()
    }
  }

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.state.user.isAuthenticated) {
      next({
        path: '/signin',
        query: {redirect: to.fullPath}, // https://stackoverflow.com/questions/45856929/redirect-to-requested-page-after-login-using-vue-router
        params: { nextUrl: to.fullPath } //FIXME: needs to actually work
      });
    } else if (store.state.user.info.permission < 1) {
      // If user is not activated yet ask them to activate account
      next({ path: '/activate' });
    } else {
      next();
    }
  } else {
    next();
  }
  store.commit('user/setIsLoading', false);
});


router.beforeEach((to, from, next) => {
  document.title = to.meta && to.meta.title || DEFAULT_TITLE
  next()
})

export default router;
