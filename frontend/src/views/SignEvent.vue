<template>
  <div>
    <EventCodeDisplay :eid="eid" />
    <h1>Welcome to {{ this.eventName }}!</h1>
    <label class="form-container">
      <form @submit="submitForm">
        <div class="label-input-div">
          <label for>zID</label>
          <input type="text" v-model="zid" />
        </div>
        <label class="label-input-div">
          <label for>Name</label>
          <input type="text" v-model="name" />
        </label>
        <button class="btn btn-primary">Sign attendance</button>
      </form>
    </label>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
import router from '@/router/index.js';
import EventCodeDisplay from "@/components/EventCodeDisplay.vue";

export default {
    name: "SignEvent",
    props: {
        eid: String
    },
    components: {
      EventCodeDisplay
    },
    created() {
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
                router.push({name: "user", params: {zid: this.zid}})
            })
            .catch(e => alert(e))
        }
    }
  };
</script>

<style scoped>
  h2 {
    text-align: center;
  }
  .form-container {
    margin-top: 3rem;
  }
</style>