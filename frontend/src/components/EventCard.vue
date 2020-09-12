<template>
  <div
    :class="[{ 'card-clickable': data._link !== undefined }]"
    class="card m-1"
    @click="clickedCard"
  >
    <img class="card-img-top" 
         :src="data.photo || 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyODAiIGhlaWdodD0iMTgwIj48cmVjdCB3aWR0aD0iMjgwIiBoZWlnaHQ9IjE4MCIgc3R5bGU9ImZpbGw6I2RlZGVkZTsiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1zaXplPSIxOCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJtb25vc3BhY2UsIHNhbnMtc2VyaWYiIGZpbGw9IiM1NTU1NTUiPng8L3RleHQ+PC9zdmc+'" 
         @error="imgAlt"
         alt="Events photo">
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
    },
    imgAlt(event) {
      event.target.src = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyODAiIGhlaWdodD0iMTgwIj48cmVjdCB3aWR0aD0iMjgwIiBoZWlnaHQ9IjE4MCIgc3R5bGU9ImZpbGw6I2RlZGVkZTsiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1zaXplPSIxOCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgYWxpZ25tZW50LWJhc2VsaW5lPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJtb25vc3BhY2UsIHNhbnMtc2VyaWYiIGZpbGw9IiM1NTU1NTUiPng8L3RleHQ+PC9zdmc+"
    },
  }
};
</script>

<style scoped>
.card {
  border: 2px solid var(--c-secondary-dark);
  width: 250px;
  box-shadow: 0 0 1rem 0rem rgba(0, 0, 0, 0.2);
}
.card-img-top {
  height: 180px;
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