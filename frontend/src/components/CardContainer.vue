<template>
  <div>
    <div class="d-flex justify-content-between py-2">
      <h3>
        {{ title }}
      </h3>
      <div>
        <slot name="options" />
      </div>
    </div>
    <div
      class="d-flex flex-wrap"
    >
      <!-- :class="viewAllData ? 'viewAllCards' : ''" -->
      <FormError
        v-if="error"
        :msg="error"
      /> 
      <Loader v-else-if="loading" />
      <slot v-else />
    </div>
  </div>
</template>
<script>
import Loader from "@/components/Loader.vue";
import FormError from '@/components/FormError.vue'
export default {
  components: {
    Loader,FormError
  },
  props: {
    error: {
      type: String,
      default: ''
    },
    loading: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    }
  }

}
</script>

<style>

</style>