<template>
  <input 
    @change="onChange"
  >
</template>

<script>
import Tagify from '@yaireo/tagify/dist/tagify.min.js'
import '@yaireo/tagify/dist/tagify.css'

export default {
  name: "Tagify",
  props: {
    settings: {
      type: Object,
      default: () => ({})
    },
    value: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      tagify: null
    }
  },
  mounted() {
    this.tagify = new Tagify(this.$el, this.settings)
  },
  watch: {
    value(n) {
      n.forEach(t => {
        if (this.tagify.value.filter(e => e.id === t.id).length === 0){
          this.tagify.addTags([t])
        }
      });
    }
  },
  methods: {
    onChange() {
      this.$emit('input',this.tagify.value)
    }
  }
}
</script>