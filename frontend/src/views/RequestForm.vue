<template>
  <Form
    @submit="submitRequest"
  >
    <template #header>
      <h2>Request</h2>
      <FormError
        v-if="error"
        :msg="error"
      />
    </template>
    <InputModule
      v-model="title"
      required
      label="Title"
    />
    <!-- <div class="label-input-div">
        <label class="label input--checkbox-label">Remember me</label>
        <input v-model="rememberUser" class="input input--checkbox" type="checkbox" />
            </div>-->
    <InputModule
      v-model="requestSelection"
      required
      label="Contact reason"
      type="select"
      :options="availableRequest"
    />

    <InputModule
      v-model="societyName"
      label="Society Name (optional)"
    />

    <InputModule
      v-model="message"
      required
      label="Message"
      type="textarea"
    />

    <template #footer>
      <button
        v-if="status === ''"
        type="submit"
        class="btn btn-primary"
      >
        Request
      </button>
      <h3 v-else>
        Success!
      </h3>
    </template>
  </Form>
</template>

<script>
import InputModule from "@/components/input/Input.vue";
import Form from "@/components/Form.vue";
import axios from "axios"
export default {
  name: "RequestForm",
  components: {
    InputModule,
    Form
  },
  props: {
    request: {
      type:String,
      default: ''
    }

  },
  data() {
    return {
      title: "",
      error: "",
      requestSelection: this.request,
      availableRequest: [
        { label: "Add my society", value: "addSoc" },
        { label: "Name change", value: "nameChange" },
        { label: "I'm not an admin to my society", value: "addAdmin" },
        { label: "There's a bug to our site", value: "bug" },
        { label: "I want to add/change something", value: "changeRequest/feature" },
        { label: "Complaint", value: "haters" },
        { label: "Others", value: "other" },
        { label: "Just want to make friends", value: "lovers" }
      ],
      message: "",
      societyName: "",
      status: ""
    };
  },
  methods: {
    submitRequest() {

      axios.post('/api/other/enquire',{
        message: JSON.stringify({
          title: this.title,
          requestSelection: this.requestSelection,
          societyName: this.societyName,
          message: this.message
        })
      })
        .then(() => {
          this.status = 'success'
        })
    }
  }
};
</script>

<style scoped>
h3 {
    display: block;
    margin: 1rem auto;
    
}
</style>