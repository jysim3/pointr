<template>
    <div>
        <h1>pointer</h1>
        <h2>Create Event</h2>
        <form @submit="submitForm">
            <div class="label-input-div">
                <label for="">Event title</label>
                <input v-bind="title" type="text">
            </div>
            <div class="label-input-div">
                <label for="">Society</label>
                <input v-bind="society" type="text">
            </div>
            <div class="label-input-div">
                <label for="">Set default points</label>
                <input v-bind="point" type="text">
            </div>
            <div class="label-input-div">
                <label for="">Show QR Code/Event link</label>
                <input type="checkbox">
            </div>

            <button @click="submitForm" class="btn-primary">Create Event</button>
        </form>
    </div>
</template>

<script>
export default {
    name: 'CreateEvent',
    methods: {
        submit(e) {
            e.preventDefault();


        }
    }
}
</script>

<style>
    .label-input-div label {
        display: block;
    }
</style>