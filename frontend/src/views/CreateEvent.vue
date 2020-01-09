<template>
  <div>
    <Logo />
    <div class="form-container">
      <form id="create-event-form" @submit.prevent="submitEventForm">
        <h2>Create an event</h2>
        <div class="label-input-div">
          <label for>Event title</label>
          <input v-model="title" type="text" required/>
        </div>
        <div class="label-input-div">
          <label for>Society</label>
          <input v-model="society" type="text" required/>
        </div>
        <div class="label-input-div">
          <label for>Set default points</label>
          <input v-model="point" type="text" required/>
        </div>
        <div class="label-input-div">
            <label for>Show QR Code/Event link</label>
            <input type="checkbox" checked/>
        </div>
        <button type="submit" class="btn btn-primary">Create Event</button>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from '@/util.js';
import router from '@/router/index.js';
import Logo from '@/components/Logo.vue';

export default {
    name: 'CreateEvent',
    components: {
      Logo
    },
    data() {
        return {
            title: "",
            society: "",
            point: 1
        }
    },
    methods: {
        submitEventForm() {
            const data = {
                name: this.title,
                owner: "Ivan",
                defaultPoints: this.point,
                zID: 'adsfh',
                eventDate: '19700201'
            }
            fetchAPI('/api/event', 'POST', data)
            .then(j => {
                console.log(j)//eslint-disable-line
                router.push({name: "event", params: {eid: j.eventID}})
            }) 

        }
    }
};
</script>

<style scoped>
@import "../assets/style.css";
</style>