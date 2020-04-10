<template>
    <div>
        <EventEnterCode v-if="!eventID" />
        <div v-else-if="isAdmin">
            <EventHostView :eventID="eventID"/>
        </div>
        <div v-else> 
            <EventSign :eventID="eventID" />
        </div>
    </div>
</template>
<script>
import EventEnterCode from "@/components/eventSign/EventEnterCode.vue";
import EventSign from "@/components/eventSign/EventSign.vue";
import EventHostView from "@/views/EventHostView.vue"
import { mapGetters } from "vuex"
import { fetchAPI } from "@/util"
export default {
    name: "Event",
    props: {
        eventID: String
    },
    components: {
        EventHostView, EventSign, EventEnterCode
    },
    data() {
        return {
            eventData: {} 
        }
    },
    created() {
      fetchAPI(`/api/event/?eventID=${this.eventID}`, "GET")
      .then(v => {
        this.eventData = v.data
        this.loading = true
      })
      .catch(e => {
        console.log(e) // eslint-disable-line
      })
    },
    computed: {
        ...mapGetters('user', [
            'event', 'isSocietyAdmin'
        ]),
        isAdmin () {
            return this.isSocietyAdmin(this.eventData.societyID)
        }
    }
}
</script>
<style scoped>

</style>