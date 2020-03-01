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
import { fetchAPI } from "@/util";
export default {
    name:"EventAdminAttendance",
    props: {
        eventID: String,
    },
    data() {
        return ({
        zID: "",
        uname: ""
        })
    },
  methods: {
    submitEventAttendance() {
      const data = {
        zID: this.zID,
        name: this.uname,
        eventID: this.eventID
      };
      fetchAPI("/api/event/signAttendanceAdmin", "POST", data)
        .then(() => {
          this.zID = "";
          this.uname = "";
        })
        .then(() => this.fetchAttendees())
        .catch(e => alert(e));
    },
  }
}
</script>
<style scoped>

#event-form-container {
  display: inline-block;
}
</style>