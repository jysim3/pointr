<template>
  <div class="container">
    <Form
      @submit="submitEventCodeForm"
    >
      <template #header>
        <h2>Enter event code</h2>
        <FormError
          v-show="formErrorMessage"
          :msg="formErrorMessage"
        />
      </template>
      <!-- TODO: sanitise input, using quotes does not work -->
      <InputModule
        v-model="eventID"
        required
        name="eventID"
        label="Event code"
        type="text"
      />
      <template #footer>
        <button
          :to="`/sign/${eventID}`"
          class="btn btn-primary"
          type="submit"
        >
          Next
        </button>
      </template>
    </Form>
  </div>
</template>

<script>
import FormError from "@/components/FormError.vue";
import InputModule from "@/components/input/Input.vue";
import Form from "@/components/Form.vue";

export default {
  name: "EventSignEnterCode",
  components: {
    Form,
    InputModule,
    FormError,
  },
  data() {
    return {
      eventID: "",
      formErrorMessage: "",
      allEventID: []
    };
  },
  methods: {
    submitEventCodeForm() {
      this.$router.push({ name: "event", params: { eventID: this.eventID } });
    }
  }
};
</script>

<style scoped>
#form-container--entercode {
  margin-top: 3rem;
}
</style>