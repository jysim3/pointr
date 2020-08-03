import EventCreate from '@/views/EventCreate.vue';
import Event from '@/views/Event.vue';
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
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Event Select - Pointr'
    }
  },
  {
    path: '/event/:eventID',
    name: 'event',
    component: Event,
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Event Page - Pointr'
    }
  },
]
