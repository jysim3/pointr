<template>
    <div>
        <EventQRCode v-bind:eid="this.eid" />
    </div>
</template>

<script>
import EventQRCode from '../components/EventQRCode.vue'

export default {
    name: 'Event',
    props: ['eid'],
    components: {
        EventQRCode
    }
}
</script>