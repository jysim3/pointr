<template>
<div>
    {{this.zid}}
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
            username: ''
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
            .then(j => console.log(j))// eslint-disable-line
            .catch(e => alert("Backend has errors, please try again\nError: " + e));
    }

    
}
</script>
<style scoped>

</style>