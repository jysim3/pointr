<template>
  <div>
    <h1>Welcome to {{ this.eventName }}!</h1>
    <form @submit="submitForm">
      <label class="inp">
        <span class="label">zid</span>
        <input type="text" v-model="zid" />
      </label>
      <br />
      <label class="inp">
        <span class="label">Name</span>
        <input type="text" v-model="name" />
        <input type="submit" />
      </label>
    </form>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
export default {
    name: "hi",
    props: {
        eid: String
    },
    mounted() {
        fetchAPI(`/api/event?eventID=${this.eid}`, "GET")
        .then(j => {
            this.eventName = j.name
        })
    },
    data() {
        return {
            zid: "",
            name: "",
            eventName: ""
        };
    },
    methods: {
        submitForm(e) {
            const data = 
            {
                zID: this.zid,
                name: this.name,
                eventID: this.eid
            }
            e.preventDefault();
            fetchAPI("/api/attend", "POST", data)
            .then(() => {
                window.location.path = "/u/"+this.zid
            })
            .catch(e => alert(e))
        }
    }
};
</script>
<style scoped></style>