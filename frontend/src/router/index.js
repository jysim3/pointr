import Vue from 'vue';
import VueRouter from 'vue-router';
import { isAuthenticated } from "@/util.js";
import Home from '@/views/Home.vue';
import EventCreate from '@/views/EventCreate.vue';
import Event from '@/views/Event.vue';
import EventSign from '@/views/EventSign.vue';
import SignIn from '@/views/auth/SignIn.vue';
import SignUp from '@/views/auth/SignUp.vue';
import SocietyJoin from "@/views/SocietyJoin.vue";
import AccountActivation from "@/views/auth/AccountActivation.vue";
import Contact from "@/views/Contact.vue";

Vue.use(VueRouter);

const routes = [
  // mode: 'history',
  // base: process.env.BASE_URL,
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/create',
    name: 'create',
    component: EventCreate,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/event/:eid',
    name: 'event',
    component: Event,
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/sign/:eid?',
    name: 'eventSign',
    component: EventSign,
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/signin',
    name: 'signIn',
    component: SignIn
  },
  {
    path: '/signup',
    name: 'signUp',
    component: SignUp
  },
  {
    path: '/joinsociety',
    name: 'joinSociety',
    component: SocietyJoin,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/activate/:activateToken',
    name: 'activate',
    component: AccountActivation,
    props: true
  },
  {
    path: '/contact',
    component: Contact
  }
];

const router = new VueRouter({
  routes
});

// For more info regarding this visit: 
// https://www.digitalocean.com/community/tutorials/how-to-set-up-vue-js-authentication-and-route-handling-using-vue-router
router.beforeEach((to, from, next) => {
  // TODO: clean up the else statements?
  // TODO: what if user goes sign in -> sign up from link in sign in form, then they may not end up at original, intended path
  // EXAMPLE: user with no account scans QR code on Event page
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated()) {
      next({
        path: '/signin',
        params: { nextUrl: to.fullPath }
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
