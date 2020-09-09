<template>
  <div
    :class="[{ 'card-clickable': data._link !== undefined }]"
    class="card m-1"
    @click="clickedCard"
  >
    <img class="card-img-top" :src="data.photo || 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22286%22%20height%3D%22180%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20286%20180%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_1747324db35%20text%20%7B%20fill%3Argba(255%2C255%2C255%2C.75)%3Bfont-weight%3Anormal%3Bfont-family%3AHelvetica%2C%20monospace%3Bfont-size%3A14pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_1747324db35%22%3E%3Crect%20width%3D%22286%22%20height%3D%22180%22%20fill%3D%22%23777%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%22107.1953125%22%20y%3D%2296.3%22%3E286x180%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E'" alt="Events photo">
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