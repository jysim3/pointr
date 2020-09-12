<template>
  <div>
    <div class="bg-white landing">
      <!-- <img src="../assets/logo.png" /> -->
      <div class="container wrapper text-center text-lg-left">
        <div class="row">
          <div class="col-lg-8 col-12">
            <h1 class="heading">
              Welcome to 
              <img
                class="logo"
                src="../assets/logo.png"
                alt="pointr logo"
              >
            </h1>
            <h3 class="sub-heading">
              The attendance tracking system for UNSW Arc Societies.
            </h3>
            <p>Mark your members' attendance in seconds and visualize them in informative graphs </p>
            <div class="btn-container">
              <router-link
                tag="button"
                to="/create"
                class="btn btn-primary"
              >
                Create an event
              </router-link>
              <router-link
                tag="button"
                to="/signup"
                class="btn btn-secondary"
              >
                Mark my attendance
              </router-link>
            </div>
          </div>
          <div class="col w-100" />
          <div class="col-lg-3 col-12">
            <EventCode event-i-d="TEST1" />
          </div>
        </div>
      </div>
    </div>
    <div class="user-tutorial container-fluid">
      <div class="container">
        <div class="user-tutorial-left"> 
          <img src="@/assets/userTutorial.png">
        </div>
        <div class="user-tutorial-right"> 
          <h1> How it works </h1>
          <p> Sign in to any events by just scanning the QR code! It’s that simple! </p>
          <div>
            <router-link
              to="/signin"
              class="btn btn-primary"
            >
              Try it now
            </router-link>
            <router-link
              to="/signup"
              class="btn btn-secondary"
            >
              View events
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <div class="admin-tutorial container-fluid">
      <h1> How it works </h1>
      <hr style="width: 10rem;">
      <div class="admin-tutorial-steps">
        <div>
          <img src="@/assets/adminTutorial1.png">
          <p>1. Create an event through your society page</p>
        </div>
        <div>
          <img src="@/assets/adminTutorial2.png">
          <p>2. Share the QR code to your members </p>
        </div>
        <div>
          <img src="@/assets/adminTutorial3.png">
          <p>3. View your attendees in beautifully generated graph</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EventUpcoming from '@/components/EventUpcoming.vue'
import EventCode from "@/components/EventCode.vue";
export default {
  name: "LandingPage",
  components: {
    EventCode,
    EventUpcoming // eslint-disable-line
  }
};
</script>

<style scoped>
.landing {
  margin-top: -3rem;
  background-image: url('~@/assets/white-background.jpg');
  background-size: cover;
  background-repeat: no-repeat;
}
.wrapper {
  padding: 10rem 0;
}
.landing-background {
  background-image: url('~@/assets/unsw.jpg');
  background-repeat: no-repeat;
  background-clip: content-box;
  background-size: cover;
}
.heading {
  color: black;
}
.user-tutorial {
  background-color: white;
  padding: 5rem ;
  background: url('~@/assets/userTutorialBackground.png');
}
.user-tutorial .container {
  display: flex;
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
@media only screen and (max-width: 900px) {
  .user-tutorial .container {
    flex-wrap: wrap;
    justify-content: center;
  }
  .user-tutorial-right * {
    text-align: center;
  }
  .admin-tutorial-steps {
    flex-wrap: wrap;
  }
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
