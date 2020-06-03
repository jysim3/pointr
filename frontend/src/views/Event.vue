<template>
    <div>

        <EventSelect v-if="!eventID"/>
        <div v-else>

            <EventHostView 
            v-if="isAdmin"
            :eventID="eventID"
            :eventData="eventData"
            />
            <EventSign 
            v-else
            :eventID="eventID" 
            :eventData="eventData"
            />
        </div>
        <div > 
        </div>
    </div>
</template>
<script>
import EventSelect from '@/components/EventSelect'
import EventSign from "@/components/eventSign/EventSign.vue";
import EventHostView from "@/views/EventHostView.vue"
import axios from 'axios'
export default {
    name: "Event",
    props: {
        eventID: String
    },
    components: {
        EventHostView, 
        EventSign, 
        EventSelect 
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
                this.isAdmin = this.$store.getters['user/isSocietyAdmin'](data.society.map(s => s.id))
            })
            .catch(c => console.log(c))
            .finally(() => this.$store.commit('loading',false))
        }
    },
    
    mounted() {
        this.getEventInfo()
    },
}
</script>
<style scoped>

</style>