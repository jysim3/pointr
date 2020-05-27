<template>
  <div @click="clickedCard" :class="{ 'event-card-clickable': data._link !== undefined }" class="event-card">
    <!-- TODO: going to an event should only be available to admin? -->
    <!-- <router-link :to="`/event/${data.eventID}`">
      <h3>{{ data.eventName }}</h3>
      <p class="event-info">by {{ data.societyName }} @ <b>{{ data.location }}</b></p>
      <p class="event-info">On {{ data.eventDate }}</p>
    </router-link> -->
    <!-- TODO: check backend, eventName/name doesn't seem to be consistent depending on request -->
    <!-- TODO: if  -->
    <div  class="tags" v-if="data.tags">
      <div class="primary">{{ data.tags[0] }}</div>

      <div>@ {{ data.tags[1] }}</div>
    </div>
    <h3 class="title">{{ data.title }}</h3>
    <p class="subtitle">{{ data.subtitle }}</p>
  </div>
</template>

<script>
export default {
  name: "EventCard",
  props: {
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
/* TODO: clean up this CSS */
/* a {
  font-weight: normal;
}
.event-card {
  border-top: 3px solid var(--c-secondary-dark);
  padding: 1rem;
}

.event-info {
  margin: 1rem 0;
} */
.event-card {
  border: 3px solid var(--c-secondary-dark);
  margin: 1rem 0.5rem ;
  padding: 1rem 1rem 1.25rem 1rem;
  border-radius: var(--border-radius);
  display: flexbox;
  flex-direction: column;
  align-items: flex-start;
  transition: 0.2s box-shadow;
  background: white;


  flex: 1 1 auto;
  white-space: nowrap;
  max-width: 250px;
  height: 100px;
  overflow: hidden;
}

.event-card:hover {
  box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.1);
}

.tags {
  margin-bottom: 1rem;
  display: flex;
  flex-wrap: wrap;
}

.tags > *:nth-child(n+2) {
  padding-left: 0.5rem;
}

.title {
  color: black;
  margin-bottom: 0.25rem;
}

.subtitle {
  font-size: 1.1rem;
}

.event-card-clickable {
  cursor: pointer;
}
</style>