<template>
  <div
    :class="[{ 'card-clickable': data._link !== undefined }]"
    class="card m-1"
    @click="clickedCard"
  >
    <div class="card-body ">
      <h5
        :class="full ? '' : 'card-title-sml'"
      >
        {{ data.title }}
      </h5>
      <h6 class="subtitle">
        {{ data.subtitle }}
      </h6>
      <div
        v-if="data.tags"
        class="tags"
      >
        <div class="primary">
          {{ data.tags[0] }}
        </div>

        <div>{{ data.tags[1] }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "EventCard",
  props: {
    full: {
      type: Boolean,
      default: false
    },
    data: {
      type: Object,
      required: true
    }
  },
  methods: {
    clickedCard() {
      if (this.data._link) {
        this.$router.push(this.data._link);
      }
    }
  }
};
</script>

<style scoped>
.card {
  border: 2px solid var(--c-secondary-dark);
  width: 250px;
  box-shadow: 0 0 1rem 0rem rgba(0, 0, 0, 0.2);
}
.card-clickable:hover {
  transform: translateY(-10px)
}
.card-clickable {
  cursor: pointer;
  transition: 0.5s all;

}
.card-title-sml {
  line-height: 1;
    height: 2em;       /* height is 2x line-height, so two lines will display */
    overflow: hidden;  /* prevents extra lines from being visible */

}
.subtitle {
  overflow: hidden;
  max-height: 2.5rem;
  /* text-overflow: ellipsis; */
  /* white-space: nowrap; */
}
</style>