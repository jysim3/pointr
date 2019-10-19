<template>
    <div>
       <h1> ajsdkfljasdklf</h1> 
    </div>
</template>

<script>
import fetchAPI from '@/util.js'
import { apiURL } from "@/util.js"

export default {
    name: 'Attendees',
    props: ['eid'],
    data() {

        return {
            attendees: '',
            name: ''
        }
    },
    mounted() {
    }
}
</script>

<style>
    
</style>