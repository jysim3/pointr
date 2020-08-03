<template>
  <div class="container">
    <div
      v-if="isSocietyAdmin"
      class="row"
    >
      <div class="box col mx-3 d-flex flex-column align-items-center">
        <h2>Actions</h2>
        <router-link
          :to="{name:'create'}"
          class="btn btn-primary"
        >
          Create an event
        </router-link>
        <router-link
          :to="{name:'editSociety'}"
          class="btn btn-primary"
        >
          Edit Society Details
        </router-link>
      </div>
      <MakeAdmin
        class="col mx-3"
        :soc-i-d="socID"
      />
    </div>
    <div
      v-else
      class="box col"
    >
      <p>Are you an admin to this society?</p> 
      <p>
        Contact us 
        <router-link :to="{name:'request', params:{request:'addAdmin'}}">
          here
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>
import MakeAdmin from "@/components/MakeAdmin.vue";
export default {
  components: {
    MakeAdmin,
  },
  props: {
    socID: {
      type: String,
      required: true
    }
  },
  computed: {
    isSocietyAdmin() { return this.$store.getters['user/isSocietyAdmin'](this.socID) },
  }

}
</script>

<style>

</style>