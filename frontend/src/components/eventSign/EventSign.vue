<template>
  <div class="container">
    <Form
      @submit="submitEventSignAttendance"
    >
      <template #header>
        <h2>Sign attendance</h2>
        <FormError
          v-if="error"
          :msg="error"
        />
      </template>

      <EventCard
        :full="true"
        :data="cardData"
      />
      <Input
        v-model="code"
        label="PIN"
        name="code"
        type="text"
      />
      <template #footer>
        <button
          v-if="!eventSignSuccess"
          class="btn btn-primary"
          type="submit"
        >
          Sign as {{ $store.state.user.name }} ({{ $store.state.user.zID }})
        </button>
        <div
          v-else
          id="submit-message"
        >
          <h3 v-if="eventAlreadySigned">
            Already signed this event!
          </h3>
          <h3 v-else>
            Success!
          </h3>
          <!-- TODO: need padding/margin on this -->
          <router-link
            id="link--home"
            to="/"
          >
            Go to home
          </router-link>
        </div>
      </template>
    </Form>
  </div>
</template>
<script>
import axios from 'axios'
import EventCard from "@/components/EventCard.vue";
import Form from "@/components/Form.vue"
import FormError from "@/components/FormError.vue"
import Input from "@/components/input/Input.vue"

export default {
  name: "EventSignEnterAttendance",
  components: {
    Input,
    EventCard,
    Form,
    FormError,
  },
  props: {
    eventID: {
      type: String,
      required: true
    },
    eventData: {
      type: Object,
      required: true
    },
    givenCode: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      loading: false,
      eventSignSuccess: false,
      eventAlreadySigned: false,
      error: "",
      code: this.givenCode,
    };
  },
  computed: {
    cardData() {
      return {
        title: this.eventData.name,
        subtitle: this.eventData.description,
        tags: [
          this.eventData.start, this.eventData.location
        ],
        _link: undefined // `/event/${this.eventData.eventID}`
      }
    }
  },
  methods: {
    submitEventSignAttendance() {
      this.error = ""
      axios({
        url: "/api/event/attend", 
        method: "POST", 
        params: {
          eventID: this.eventID,
          code: this.code
        }
      }).then(() => {
        this.eventSignSuccess = true;
      })
        .catch(e => {
          console.log(!e.response.data.message.code)
          if (e.response && e.response.data && e.response.data.message){
            if  (e.response.data.message.code) {
              this.error = "Your PIN is invalid, please try again."
            } else if (e.response.data.message === "Already Attended") {
              this.eventSignSuccess = true;
            }
            return
          }
          this.error = "Sorry you are not able to sign in for now. Try again later"
        }); 
    }
  }
};
</script>

