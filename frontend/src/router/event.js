import EventCreate from '@/views/EventCreate.vue';
import Event from '@/views/Event.vue';
import store from '@/store/index';
import EventSelect from '@/views/EventSelect.vue';
export default  [
  {
    path: '/create',
    name: 'create',
    component: EventCreate,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Create Event - Pointr'
    }
  },
  {
    path: '/edit/:eventID',
    name: 'edit',
    component: EventCreate,
    props: true,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Edit Event - Pointr'
    }
  },
  {
    path: '/event',
    name: 'eventSelect',
    component: EventSelect,
    props:  route => ({queryTags: route.query.tags -1 + 1}),
    meta: {
      requiresAuth: true,
      title: 'Event Select - Pointr'
    }
  },
  {
    path: '/event/:eventID',
    name: 'event',
    component: Event,
    props: route => ({ 
      eventID: route.params.eventID, 
      code: route.query.code,
      expiryTime: route.query.expiryTime,
      newUser: !store.getters.isAuthenticated,
    }),
    meta: {
      title: 'Event Page - Pointr'
    }
  },
]
