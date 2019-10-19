<template>
<div>
    <h1> Thanks for attending, {{this.username}} </h1>
    <table>
        <tr v-for="(event,index) in events" :key="index">
            <td>{{ event.name }}</td>
            <td>{{ event.points }}</td>
        </tr>
    </table>
</div>
</template>
<script>
import {fetchAPI} from '@/util.js'
export default {
    name: "User",
    props: {
        zid: String
    },
    data() {
        return {
            username: 'Steven',
            events: [
                {
                    name: "Coffee Night #2",
                    points: 5
                },
                {
                    name: "Coffee Night #3",
                    points: 5
                },
            ]

        }
    },
    mounted() {
        
        fetchAPI(`/api/user?zID=${this.zid}`, "GET")
        .then(j => {
            console.log(j)// eslint-disable-line
            this.events=j
        })
    }

    
}
</script>
<style scoped>

</style>