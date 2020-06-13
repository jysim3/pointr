// import SocietyJoin from '@/views/SocietyJoin.vue';
import Society from '@/views/SocietyPage.vue';
import SelectSociety from '@/views/SelectSociety.vue';
export default [
  {
    path: '/society/:socID',
    name: 'society',
    component: Society,
    // TODO: make this available for public?
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Society Page - Pointr'
    }
  },
  {
    path: '/society',
    name: 'society',
    component: SelectSociety,
    // TODO: make this available for public?
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Society Page - Pointr'
    }
  },
]