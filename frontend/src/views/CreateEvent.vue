<template>
    <div>
        <h1>pointer</h1>
        <h2>Create Event</h2>
        <form action="">
            <div class="label-input-div">
                <label for="">Event title</label>
                <input type="text">
            </div>
            <div class="label-input-div">
                <label for="">Society</label>
                <input type="text">
            </div>
            <div class="label-input-div">
                <label for="">Set default points</label>
                <input type="text">
            </div>
            <div class="label-input-div">
                <label for="">Show QR Code/Event link</label>
                <input type="checkbox">
            </div>

            <button class="btn-primary">Create Event</button>
        </form>
    </div>
</template>

<script>
export default {
    name: 'CreateEvent'
}
</script>

<style>
    .label-input-div label {
        display: block;
    }
</style>