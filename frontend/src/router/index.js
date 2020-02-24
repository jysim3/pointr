import Vue from 'vue';
import VueRouter from 'vue-router';
import { isAuthenticated } from "@/util.js";
import Home from '@/views/Home.vue';
import EventCreate from '@/views/EventCreate.vue';
import Event from '@/views/Event.vue';
import SignEvent from '@/views/SignEvent.vue';
import User from '@/views/User.vue';
import MarkAttendance from '@/views/MarkAttendance.vue';
import SignIn from '@/views/auth/SignIn.vue';
import SignUp from '@/views/auth/SignUp.vue';
import SocietyJoin from "@/views/SocietyJoin.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
    // TODO: depending on whether there is token, have profile/dashboard as page
  },
  {
    path: '/mark-attendance',
    name: 'markAttendance',
    component: MarkAttendance,
    meta: {
      requiresAuth: true
    }
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
    path: '/u/:zid',
    name: 'user',
    component: User,
    props: true,
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
    path: '/e/:eid',
    name: 'signEvent',
    component: SignEvent,
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
  }
];

const router = new VueRouter({
  routes
});

// For more info regarding this visit: 
// https://www.digitalocean.com/community/tutorials/how-to-set-up-vue-js-authentication-and-route-handling-using-vue-router
router.beforeEach((to, from, next) => {
  // TODO: clean up the else statements?
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
