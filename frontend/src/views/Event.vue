<template>
  <div>
    <EventHostView 
      v-if="isAdmin"
      :event-i-d="eventID"
      :event-data="eventData"
    />
    <EventSign 
      v-else
      :given-code="code"
      :event-i-d="eventID" 
      :event-data="eventData"
      :sign-form="newUser"
      :expiry-time="expiryTime"
    />
  </div>
</template>
<script>
import EventSign from "@/components/eventSign/EventSign.vue";
import EventHostView from "@/views/EventHostView.vue"
import { getEvent } from '@/api/event';
export default {
  name: "Event",
  components: {
    EventHostView, 
    EventSign, 
  },
  props: {
    code: {
      type: String,
    },
    eventID: {
      type: String,
      required: true
    },
    newUser: {
      type: Boolean,
      required: true
    },
    expiryTime: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      eventData: {
        description: "",
        end: "",
        hasAccessCode: false,
        hasAdminSignin: false,
        hasQR: false,
        id: "",
        location: null,
        name: "",
        photos: null,
        preview: null,
        society: [""],
        start: "",
        status: 0,
      } ,
      loading: false,
      name: '',
      description: '',
      isAdmin: false,
    }
  },
  watch: {
    eventID(v) {
      if (v) {
        this.getEventInfo()
      }
    }
  },
    
  mounted() {
    this.getEventInfo()
    console.log(this.newUser)
  },
  methods: {

    getEventInfo() { 
      if (!this.eventID){
        return
      }
      this.$store.commit('loading',true)
      getEvent(this.eventID)
        .then(data => {
          Object.assign(this.eventData, data)
          this.isAdmin = this.$store.getters['user/isSocietyAdmin'](data.society.map(s => s.id))
        })
        .catch(e => {
          console.log(e)
        })
        .finally(() => this.$store.commit('loading',false))
    }
  },
}
</script>
<style scoped>

</style>
