<template>
  <div>
    <div class="landing-background">
      <div class="container wrapper">
        <!-- <img src="../assets/logo.png" /> -->
        <div>
          <h1 class="heading">Welcome to Pointr!</h1>
          <h3 class="sub-heading">The event tracking system for UNSW societies.</h3>
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
    <div class="user-tutorial container-fluid">
      <div class="container">
        <div class="user-tutorial-left"> 
          <img src="@/assets/userTutorial.png"/>
        </div>
        <div class="user-tutorial-right"> 
          <h1> How it works </h1>
          <p> Sign in to any events by just scanning the QR code! It’s that simple! </p>
          <div>
            <router-link to="/signin" class="btn btn-primary" > Try it now </router-link>
            <router-link to="/event" class="btn btn-secondary" >View events</router-link>
          </div>
        </div>
      </div>
    </div>
    <div class="admin-tutorial container-fluid">
        <h1> How it works </h1>
        <hr style="width: 10rem;"/>
        <div class="admin-tutorial-steps">
          <div>
            <img src="@/assets/adminTutorial1.png" />
            <p>1. Create an event through your society page</p>
          </div>
          <div>
            <img src="@/assets/adminTutorial2.png" />
            <p>2. Share the QR code to your members </p>
          </div>
          <div>
            <img src="@/assets/adminTutorial3.png" />
            <p>3. Download the attendance list according to your needs!</p>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import EventList from '@/components/EventList.vue'
import axios from 'axios'
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
      axios.get('/api/event/upcoming')
      .then(v => {
        this.eventData = v.data.data
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
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  text-align: center;
  padding: 10rem 0;
}
.landing-background {
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
.user-tutorial {
  background-color: white;
  padding: 5rem ;
  background: url('~@/assets/userTutorialBackground.png');
}
.user-tutorial .container {
  display: flex;
  flex-wrap: nowrap;
  align-items: stretch;
  justify-content: space-between;
}
img {
  max-width: 300px;

}
.user-tutorial-right {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.user-tutorial-right * {
  text-align: right;
}
.user-tutorial-right h1 {
  margin-bottom: 2rem;
}
.user-tutorial-right div {
  margin: 3rem 0;
}
.admin-tutorial {
  background-color: white;
  padding: 5rem ;
}
.admin-tutorial-steps {
  padding-top: 5rem;
  display: flex;
  justify-content: space-around;
  align-items: stretch;
}
.admin-tutorial-steps > div {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  width: 400px;
}
.admin-tutorial-steps > div > img {
  flex-grow: 1;
  object-fit: contain;

}
.admin-tutorial-steps > div > p {
  text-align: center;
  white-space: normal;
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