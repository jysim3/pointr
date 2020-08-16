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
    />
  </div>
</template>
<script>
import EventSign from "@/components/eventSign/EventSign.vue";
import EventHostView from "@/views/EventHostView.vue"
import axios from 'axios'
import moment from 'moment'
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
  },
  methods: {

    getEventInfo() { 
      if (!this.eventID){
        return
      }
      this.$store.commit('loading',true)
      axios.get(`/api/event?eventID=${this.eventID}`)
        .then(response => {
          const data = response.data.data
          Object.assign(this.eventData, data)
          this.eventData.start = moment(this.eventData.start)
          this.eventData.end = moment(this.eventData.end)
          this.isAdmin = this.$store.getters['user/isSocietyAdmin'](data.society.map(s => s.id))
        })
        .catch(c => {
          console.log(c)
          this.$router.push({name:'404'})
        })
        .finally(() => this.$store.commit('loading',false))
    }
  },
}
</script>
<style scoped>

</style>