<template>
  <div>
    <transition
      name="fade"
      mode="out-in"
    >
      <EventFullScreen
        v-if="fullscreen" 
        :event-soc="eventSoc"
        :name="eventData.name"
        :event-i-d="eventID"
        @exit-full-screen="toggleFullScreen(false)"
      />
    </transition>
    <div
      v-show="!fullscreen"
      id="event-host-view-wrapper"
    >
      <div class="d-flex flex-column align-items-center">
        <div class="box d-flex p-3 px-5 flex-column">
          <h4 class="header">
            Event code
          </h4>
          <h2 class="code primary">
            {{ eventID }}
          </h2>
        </div>
        <h1 id="welcome-header">
          Welcome to {{ eventData.name }}
        </h1>
        by<h3 class="societies">
          {{ eventSoc }}
        </h3>
        <div>
          <button
            class="btn btn-primary"
            @click="toggleFullScreen(true)"
          >
            Full screen <i class="material-icons">fullscreen</i>
          </button>
          <router-link
            :to="{name:'edit',params: {eventID: eventID}}"
            class="btn btn-primary"
          >
            Edit event <i class="material-icons">edit</i>
          </router-link>
        </div>
      </div>
      <p class="description">
        {{ eventData.description }}
      </p>

      <!---- EVENT BODY ----->

      <h2
        class="my-4"
      >
        Sign your attendance
      </h2>
      <div class="d-flex justify-content-center">
        <EventQRCode
          class="mx-4"
          :event-i-d="eventID"
        />
        <EventAdminAttendance
          :event-i-d="eventID"
        />
      </div>
      <div>
        <EventAttendance
          :event-duration="eventDuration"
          :event-start="eventData.start"
          :event-end="eventData.end"
          :event-name="eventData.name" 
          :event-i-d="eventID"
        />
        <FormError
          v-show="error"
          :msg="error"
        />
      <!-- TODO: only show last 10 people who have joined? Click 'view all' to show all participants? -->
      </div>
    </div>
  </div>
</template>

<script>
import EventAttendance from "@/components/event/EventAttendance.vue";
import EventQRCode from "@/components/event/EventQRCode.vue";
import EventAdminAttendance from "@/components/event/EventAdminAttendance.vue";
import EventFullScreen from "@/components/EventFullScreen.vue";
import FormError from "@/components/FormError.vue";
import moment from 'moment'

export default {
  name: "EventHost",
  components: {
    EventQRCode,
    EventAttendance,
    EventAdminAttendance,
    EventFullScreen,
    FormError
  },
  props: {
    eventID: {
      type: String,
      required: true
    },
    eventData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      error: "",
      fullscreen: false
    }
  },
  computed: {
    eventDuration() {

      return moment(this.eventData.end).diff(moment(this.eventData.start),'hours')
    },
    eventSoc () {
      return this.eventData.society.map(s => s.name).join(' | ')
    },
    eventURL() {
      return `${window.location.host}/event/${this.eventID}`;
    },
    reversedParticipants() {
      const participantsCopy = this.participants.slice();
      return participantsCopy.reverse();
    }
  },
  methods: {
    toggleFullScreen(fullScreen) {
      this.$store.commit('navBar', !fullScreen)
      this.fullscreen = fullScreen
    }

  },
};
</script>

<style scoped>
/* TODO: refactor this CSS */
#event-host-view-wrapper {
  display: flex;
  flex-direction: column;
  align-content: center;
  text-align: center;
}
.societies {
  color:rgb(143, 106, 0);
  margin-top: 1rem;
}
#welcome-header {
  margin: 2rem 0;
}
.description {
  margin-top: 2rem;
  text-align: center;
}

#mark-attendance-header {
  text-align: center;
  margin: 3rem 0 2rem 0;
  font-weight: 400;
}

#event-url {
  text-transform: none;
  font-family: monospace;
}

#event-form {
  box-shadow: none;
}

#qr-container {
  display: inline-block;
}

#qr-and-form-container {
  display: flex;
  justify-content: center;
}

#qr-container {
  margin-right: 2rem;
}

.fullscreen-btn {
  margin-top: 1rem;
  justify-content: center;
}
</style>
