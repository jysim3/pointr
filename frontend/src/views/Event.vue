<template>
    <div>
        <EventEnterCode v-if="!eventID" />
        <!-- <div v-else-if="isAdmin"> -->
            <EventHostView :eventID="eventID"/>
        <!-- </div>
        <div v-else> 
            <EventSign :eventID="eventID" />
        </div> -->
    </div>
</template>
<script>
import EventEnterCode from "@/components/eventSign/EventEnterCode.vue";
// import EventSign from "@/components/eventSign/EventSign.vue";
import EventHostView from "@/views/EventHostView.vue"
// import axios from 'axios'
export default {
    name: "Event",
    props: {
        eventID: String
    },
    components: {
        EventHostView, 
        // EventSign, 
        EventEnterCode
    },
    data() {
        return {
            eventData: {} ,
            loading: false,
            isAdmin: false
        }
    },
    created() {
    },
}
</script>
<style scoped>

</style>