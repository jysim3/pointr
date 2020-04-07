<template>
  <div>
    <div class="container">
      <div class="wrapper">
        <!-- <img src="../assets/logo.png" /> -->
        <div>
          <h1 class="heading">Welcome to Pointr!</h1>
          <h3 class="sub-heading">The event tracking system for UNSW colleges.</h3>
          <div class="btn-container">
            <router-link tag="button" to="/create" class="btn btn-primary">Create an event</router-link>
            <router-link tag="button" to="/sign" class="btn btn-secondary">Mark my attendance</router-link>
          </div>
          <EventList />
        </div>
        <EventList
          :eventData="eventData"
          listStyle="table"
          eventViewTitle=""
          :loading="eventDataLoading"
        />
      </div>
    </div>
  </div>
</template>

<script>
import EventList from '@/components/EventList.vue'
import { fetchAPI } from '@/util.js'
export default {
  name: "LandingPage",
  components: {
    EventList
  },
  data () {
    return {
      eventData: [],
      eventDataLoading: false
    }
  },
  mounted() {
      this.eventDataLoading = true
      fetchAPI(`/api/event/upcomingEvents`, "GET")
      .then(v => {
        this.eventData = v.data
        this.eventDataLoading = false
      })
      .catch(e => {
        console.log(e) // eslint-disable-line
      })
  }
};
</script>

<style scoped>
.wrapper {
  width: 80%;
  margin: auto;
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  text-align: center;
  padding: 25% 0;
}
.container-alt,.container {
  background-image: url('~@/assets/unsw.jpg');
  background-repeat: no-repeat;
  background-clip: content-box;
  background-size: cover;
}
.heading {
  color: white;
}
.sub-heading {
  color: #d1d1d1;
}

.btn {
  font-size: 1rem;
  margin: 1rem;
}

.btn-container {
  display: flex;
  justify-content: center;
}
@media only screen and (max-width: 600px) {
  .left {
    display: none;
  }
  .heading,.sub-heading{
    text-align: center;
  }
  .btn-container {
    justify-content: center;
    margin: 3rem;
    flex-wrap: wrap;
  }
}
</style>