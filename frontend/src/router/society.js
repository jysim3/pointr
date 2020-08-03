// import SocietyJoin from '@/views/SocietyJoin.vue';
import Society from '@/views/SocietyPage.vue';
import SelectSociety from '@/views/SelectSociety.vue';
import SocietyEdit from '@/views/SocietyEdit.vue'
export default [
  {
    path: '/society/:socID/edit',
    name: 'editSociety',
    component: SocietyEdit,
    // TODO: make this available for public?
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Edit Society'
    }
  },
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
    name: 'selectSociety',
    component: SelectSociety,
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Society Page - Pointr'
    }
  },
]