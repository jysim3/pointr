<template>
  <div>
    <div class="container">
      <div class="row mb-5 align-content-stretch justify-content-center">
        <div class="col-4 col-md-2">
          <div class="event-date d-flex flex-column justify-content-center align-content-center text-center rounded p-1 h-100">
            <span>24</span>
            <span>Aug</span>
          </div>
        </div>
        <div class="col-6 col-md-8 event-title">
          <h2 class="">
            {{ eventData.name }}
          </h2>
          <h4 class="event-subtitle">
            by {{ eventData.society[0].name }}
          </h4>
        </div>
        <div class="col-2 col-md-2 d-flex align-content-center">
          <router-link
            :to="{name:'edit',params: {eventID: eventID}}"
            class="m-0 d-flex"
          >
            <i class="material-icons">edit</i>
          </router-link>
        </div>
      </div>
      <div class="row">
        <div
          class="col-12 col-md-9 event-photo position-relative mb-5"
        >
          <img
            class="rounded"
            src="https://scontent.fsyd9-1.fna.fbcdn.net/v/t1.0-9/s960x960/106941582_4054164364653593_2603835058121570065_o.jpg?_nc_cat=107&_nc_sid=340051&_nc_ohc=KKbbWZuZNjUAX_IrLoX&_nc_ht=scontent.fsyd9-1.fna&_nc_tp=7&oh=51bdc56aa46636ab50ef8950f2d1caf5&oe=5F5DC714"
          >
        </div>
        <div class="col-12 col-md-3 mb-5">
          <EventCode :event-i-d="eventID" />
        </div>
      </div>
      <div class="row">
        <div class="col-8">
          <h1>Details</h1>
          <div class="col mb-4">
            <div class="mb-2">
              <i class="material-icons mr-2">group</i>
              <!-- TODO: correct attendees -->
              <span>140 attendees (beta not working)</span>
            </div>
            <div class="mb-2">
              <i class="material-icons mr-2">place</i>
              <span>{{ eventData.location }}</span>
            </div>
            <div class="mb-2">
              <i class="material-icons mr-2">public</i>
              <span>Public</span>
            </div>
          </div>
          <p class="description">
            {{ eventData.description }}
          </p>
        </div>
      </div>

      <!---- EVENT BODY ----->

      <div class="row">
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
import EventCode from "@/components/EventCode.vue";
import FormError from "@/components/FormError.vue";
import moment from "moment";

export default {
  name: "EventHost",
  components: {
    EventCode,
    EventAttendance,
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
    };
  },
  computed: {
    eventDuration() {
      return moment(this.eventData.end).diff(
        moment(this.eventData.start),
        "hours"
      );
    },
  },
  methods: {
  }
};
</script>

<style scoped>
.event-subtitle {
  color: #989898;
}
.event-title {
  color: black;
}
.event-date {
  background-color: #252525;
  color: white;
}
.event-photo {
  overflow: hidden;
}
.event-photo > img{
    min-height: 100%;
    width: 100%;
    object-fit: fill;
}
@media only screen and (max-width: 600px) {
  .event-photo > img{
    min-height: auto;
    height: auto;
  }
}
</style>
