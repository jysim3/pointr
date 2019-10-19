<template>
<div>
    <h1> Hi {{this.username}} </h1>
    <table>
        <tr v-for="(event,index) in events" :key="index">
            <td>{{ event.name }}</td>
            <td>{{ event.points }}</td>
        </tr>
    </table>
</div>
</template>
<script>
import {apiURL} from '@/App.vue'
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
        
        const data = {
            "zID": this.zid
        }
        fetch(apiURL + "/api/user", {
            method: "POST", // or 'PUT'
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers: {
            "Content-Type": "application/json"
            }
        })
            .then(r => r.json())
            .then(j => {this.events=j})// eslint-disable-line
            .catch(e => alert("Backend has errors, please try again\nError: " + e));
    }

    
}
</script>
<style scoped>

</style>