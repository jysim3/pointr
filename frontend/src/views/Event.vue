<template>
    <div>
        <h2>Your event code is {{ this.eid }}</h2>
        <EventQRCode v-bind:eid="this.eid" />
        <h3>{{ eventURL }}</h3>
        <form action="">
             <div class="label-input-div">
                <label for="">Enter zID</label>
                <input type="text" required>
            </div>
            <button>Submit</button>
        </form>
    </div>
</template>

<script>
import EventQRCode from '../components/EventQRCode.vue'

export default {
    name: 'Event',
    props: ['eid'],
    components: {
        EventQRCode
    },
    computed: {
        eventURL() {
            return `${window.location.host}/e/${this.eid}`
        }
    }
}
</script>