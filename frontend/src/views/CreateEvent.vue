<template>
  <div>
    <h1>pointer</h1>
    <div class="form-container">
        <h2>Create Event</h2>
        <form @submit="submitForm">
            <div class="label-input-div">
                <label for="">Event title</label>
                <input v-model="title" type="text">
            </div>
            <div class="label-input-div">
                <label for="">Society</label>
                <input v-model="society" type="text">
            </div>
            <div class="label-input-div">
                <label for="">Set default points</label>
                <input v-model="point" type="text">
            </div>
            <div class="label-input-div">
                <label for="">Show QR Code/Event link</label>
                <input type="checkbox">
            </div>

        <button @click="submitForm" class="btn-primary">Create Event</button>
      </form>
    </div>
  </div>
</template>

<script>
import { fetchAPI } from '@/util.js';
import router from '@/router/index.js'

export default {
    name: 'CreateEvent',
    data() {
        return {
            title: "",
            society: "",
            point: 1
        }
    },
    methods: {
        submitForm(e) {
            e.preventDefault();
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
  }
};
</script>

<style>
@import "../assets/style.css";
</style>