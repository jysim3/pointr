import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store/index';
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
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/event/:eventID',
    name: 'event',
    component: Event,
    props: true,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
    // TODO: only the creator of the society/event should be able to access this, need to have function that checks they are authorized after we know they are authenticated.
  },
  {
    path: '/sign/:eventID?',
    name: 'eventSign',
    component: EventSign,
    props: true,
    meta: {
      requiresAuth: true,
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
    path: '/activate/:activateToken?',
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
  mode: 'history',
  routes
});

// For more info regarding this visit: 
// https://www.digitalocean.com/community/tutorials/how-to-set-up-vue-js-authentication-and-route-handling-using-vue-router
router.beforeEach((to, from, next) => {
  // TODO: needs to go over requiresAdmin?
  // TODO: what if user goes sign in -> sign up from link in sign in form, then they may not end up at original, intended path
  // TODO: signed in user should not be able to go to sign in or sign up
  // EXAMPLE: user with no account scans QR code on Event page
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.user.isAuthenticated) {
      next({
        path: '/signin',
        params: { nextUrl: to.fullPath } //FIXME: needs to actually work
      });
    } else if (store.user.info.permission < 1) {
      // If user is not activated yet ask them to activate account
      next({ path: '/activate' })
    } else {
      next()
    }
  } else {
    next();
  }
});

export default router;
