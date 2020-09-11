<template>
  <div class="container">
    <Form
      @submit="formSubmit"
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
      <div v-if="signForm">
        <div v-if="createUser">
          <InputZID v-model="zID" />
          <Input
            v-model="userInfo.firstName"
            name="firstName"
            type="text"
            label="First Name"
          />
          <Input
            v-model="userInfo.lastName"
            name="lastName"
            type="text"
            label="Last Name"
          />
          <InputPassword v-model="password" />
          <Input 
            v-model="userInfo.isArcMember"
            label="Are you an arc member?"
            type="checkbox"
          />
          <div class="d-flex flex-column align-items-center">
            <span>By signing up, you agree to our</span>
            <span>
              <router-link :to="{name:'privacy'}">
                privacy policy
              </router-link>
              and
              <router-link :to="{name:'terms'}" >
                terms and condition</router-link>
            </span>
            <span> Have an account? </span>
            <a
              class="link"
              @click="createUser = !createUser"
            > Log in </a>
          </div>
        </div>

        <div v-else>
          <InputZID
            v-model="zID"
            :z-i-d="zID"
          />
          <Input
            v-model="password"
            type="password"
            name="password"
            label="Password"
          />
          <div class="additional-links d-flex flex-column align-items-center">
            <span>Forgot your password?</span>
            <router-link to="/forgotPassword">
              Reset your password here
            </router-link>
            <span>Don't have an account? </span>
            <a
              class="link"
              @click="createUser = !createUser"
            > Sign up here </a>
          </div>
        </div>
        
      </div>
      <template #footer>
        <button
          v-if="!eventSignSuccess"
          class="btn btn-primary"
          type="submit"
        >
          Sign as ({{ zID }})
        </button>
        <div
          v-else
          class="d-flex flex-container align-content-center flex-column "
        >
          <h3 v-if="eventAlreadySigned">
            Already signed this event!
          </h3>
          <div v-else class="text-center">
            <h3>
              Success!
            </h3>
            <p v-if="!activated">
              Note: Your account is not activated yet. Your attendance will not count until you have activated your account 
            </p>
          </div>
          <!-- TODO: need padding/margin on this -->
          <router-link
            to="/"
            class="text-center"
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
import InputZID from "@/components/input/InputZID.vue";
import InputPassword from "@/components/input/InputNewPassword.vue";
import Input from "@/components/input/Input.vue"

export default {
  name: "EventSignEnterAttendance",
  components: {
    Input,
    EventCard,
    Form,
    FormError,
    InputPassword,
    InputZID,
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
    },
    signForm: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      eventSignSuccess: false,
      eventAlreadySigned: false,
      error: "",
      code: this.givenCode,
      zID: this.$store.getters.zID || '',
      password: "",
      createUser: true,
      userInfo: {
        firstName: "",
        lastName: "",
        preferredName: "",
        commencmentYear: this.currentYear,
        studentType: "",
        degreeType: "",
        isArcMember: false
      },
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
    },
    activated() { return  this.$store.getters.tokenInfo['permission'] !== 0}
  },
  methods: {
    formSubmit(){
      if (this.signForm) {
        this.getUser().then(() => this.submitEventSignAttendance())
          .catch(e => this.error = e)
      } else {
        this.submitEventSignAttendance()
      }

    },
    getUser() {
      return new Promise((resolve, reject) => {
        if (!this.createUser) {
          const data = {
            zID: this.zID,
            password: this.password
          };
          this.$store
            .dispatch("login", data)
            .then(() => {
              resolve()
            })
            .catch(e => {
              if (e.response) {
                reject(e.response.data.message)
              }
              reject()
            });
        } else {
          const data = {
            zID: this.zID,
            firstName: this.userInfo.firstName,
            lastName: this.userInfo.lastName,
            password: this.password,
            commencementYear: this.userInfo.commencmentYear,
            isArc: this.userInfo.isArcMember
          }
          this.$store.dispatch('auth/register',data)
            .then(() => resolve()).catch(r => {
              reject(Object.values(r.response.data.message)[0])
            })
        }
      })
    },
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

