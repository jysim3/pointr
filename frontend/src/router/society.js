import SocietyJoin from '@/views/SocietyJoin.vue';
import Society from '@/views/Society.vue';
export default [
  {
    path: '/society/join',
    name: 'joinSociety',
    component: SocietyJoin,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/society/:socID?',
    name: 'society',
    component: Society,
    // TODO: make this available for public?
    props: true,
    meta: {
      requiresAuth: true
    }
  },
]