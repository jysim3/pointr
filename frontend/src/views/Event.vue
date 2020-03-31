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
export default {
    name: "Event",
    props: {
        eventID: String
    },
    components: {
        EventHostView, EventSign, EventEnterCode
    },
    computed: {
        ...mapGetters('user', [
            'event', 'isSocietyAdmin'
        ]),
        isAdmin () {
            return this.isSocietyAdmin(this.event(this.eventID).societyID)
        }
    }
}
</script>
<style scoped>

</style>