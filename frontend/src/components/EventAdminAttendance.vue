<template>
    
    <div>
      <div id="event-form-container" class="form-container">
        <!-- TODO: Have forms be their own component with slots? -->
        <form id="event-form" class="form" @submit.prevent="submitEventAttendance">
            <label class="label" for>zID</label>
            <input class="input" v-model="zID" type="text" required />
            <label class="label" for>Name</label>
            <input class="input" v-model="uname" type="text" required />
          <button type="submit" class="btn btn-primary">Sign attendance</button>
        </form>

      </div>
    </div>
</template>
<script>
export default {
    name:"EventAdminAttendance",
    data() {
        return ({
        zID: "",
        uname: ""
        })
    }
}
</script>
<style scoped>

#event-form-container {
  display: inline-block;
}
</style>