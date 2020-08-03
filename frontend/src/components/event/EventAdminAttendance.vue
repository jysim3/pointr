<template>
  <Form
    class="mb-4"
    @submit="submitEventAttendance"
  >
    <template #header>
      <h2>Sign your member</h2>
      <FormError
        v-if="error.status"
        :msg="error.msg"
      />
    </template>
    <label
      class="label"
      for
    >zID</label>
    <input
      v-model="zID"
      class="input"
      type="text"
      required
    >
    <label
      class="label"
      for
    >Name</label>
    <input
      v-model="uname"
      class="input"
      type="text"
      required
    >
    <template #footer>
      <button
        type="submit"
        class="btn btn-primary"
      >
        Sign attendance
      </button>
    </template>
  </Form>
</template>
<script>
import axios from 'axios'
import FormError from "@/components/FormError.vue";
import Form from "@/components/Form.vue";
export default {
  name:"EventAdminAttendance",
  components: {
    FormError,
    Form
  },
  props: {
    eventID: {
      type: String,
      required: true
    },
  },
  data() {
    return ({
      signup: false,
      zID: "",
      uname: "",
      error: {
        status: false,
        msg: ""
      }
    })
  },
  methods: {
    registered(value) {
      this.zID = value.zID
      this.uname = value.name
      this.submitEventAttendance()
      this.signup = false
    },
    submitEventAttendance() {
      axios.post('/api/event/attend/admin', {}, 
        {
          params: {
            zID: this.zID,
            name: this.uname,
            eventID: this.eventID
          }

        }) .then(() => {
        this.zID = "";
        this.uname = "";
      })
        .catch(err => {
            console.log(err.response) //eslint-disable-line
          this.error.status = true;
          this.error.msg = err.response.data.message;
        });
    },
  }
}
</script>