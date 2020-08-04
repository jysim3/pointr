<template>
  <div class="row justify-content-center">
    <form 
      class="box col-lg-8 col-12 d-flex flex-column align-items-center"
      @submit.prevent="$emit('submit')"
    >
      <div 
        v-if="backLink"
        class="form-back-link"
      >
        <router-link
          :to="backLink"
          class="material-icons primary"
        >
          chevron_left
        </router-link>
      </div>
      <div class="d-flex flex-column align-items-center text-center">
        <slot name="header" />
      </div>
      <div class="row">
        <div class="form-body col-md-8 col-12 d-flex flex-column align-items-center">
          <slot class="" />
        </div>
      </div>
      <div class="form-footer d-flex flex-column align-items-center">
        <slot name="footer">
          <button
            type="submit"
            class="btn btn-primary"
          >
            Submit
          </button>
        </slot>
      </div>
    </form>
  </div>
</template>

<script>
export default {

  props: {
    backLink: {
      type: Object,
      default: null
    }
  },
  emits: ['submit']
}
</script>

<style>

</style>