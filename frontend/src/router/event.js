import EventCreate from '@/views/EventCreate.vue';
import Event from '@/views/Event.vue';
export default  [
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
    path: '/event/:eventID?',
    name: 'event',
    component: Event,
    props: true,
    meta: {
      requiresAuth: true,
    }
  },
]
