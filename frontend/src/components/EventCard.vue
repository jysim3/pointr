<template>
  <div class="event-card">
    <!-- TODO: going to an event should only be available to admin? -->
    <!-- <router-link :to="`/event/${eventData.eventID}`">
      <h3>{{ eventData.eventName }}</h3>
      <p class="event-info">by {{ eventData.societyName }} @ <b>{{ eventData.location }}</b></p>
      <p class="event-info">On {{ eventData.eventDate }}</p>
    </router-link> -->
    <!-- TODO: check backend, eventName/name doesn't seem to be consistent depending on request -->
    <!-- TODO: if  -->
    <div @click="goToEvent" :class="{ 'event-card-clickable': isAdminOfEvent }" class="when-where-div">
      <p class="when">{{ eventData.eventDate }}</p>
      <p class="where">@ {{ eventData.location }}</p>
    </div>
    <h3 class="name">{{ eventData.name }}</h3>
    <p class="society">{{ eventData.societyName }}</p>
  </div>
</template>

<script>
export default {
  name: "EventCard",
  props: {
    eventData: {
      type: Object,
      required: true
    }
  },
  computed: {
    isAdminOfEvent() {
      // TODO: actually check based on event, this depends on whether dashboard shows events attended by an admin
      return this.$store.state.user.isAdmin;
    }
  },
  methods: {
    goToEvent() {
      if (this.isAdminOfEvent) {
        const eventID = this.eventData.eventID;
        this.$router.push({ name: 'event', params: { eventID } });
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
  margin: 1rem;
  padding: 1rem 1rem 1.25rem 1rem;
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.when-where-div {
  margin-bottom: 1rem;
  display: flex;
  flex-wrap: wrap;
}

.when {
  color: var(--c-primary);
}

.where {
  padding-left: 0.5rem;
}

.name {
  color: black;
  margin-bottom: 0.25rem;
}

.society {
  font-size: 1.1rem;
}

.event-card-clickable {
  cursor: pointr;
}
</style>