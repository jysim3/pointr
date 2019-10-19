<template>
    <div>
        
    </div>
</template>

<script>
import fetchAPI from '@/util.js'
import { apiURL } from "@/util.js"

export default {
    name: 'Attendees',
    props: ['eid'],
    mounted() {
        const attendees = await fetchAPI('/dummy/event?eventID=' + this.eid)
    }
}
</script>

<style>
    
</style>