<template>
  <div>
    <Form
      :back-link="{name:'society',params: {socID}}"
      @submit="submitEventForm"
    >
      <template #header>
        <h2>Edit society Details</h2>
      </template>


      <InputModule
        v-model="name" 
        required 
        name="name" 
        label="Society Name" 
        type="input"
      />

      <InputModule
        v-model="description" 
        required 
        name="description" 
        label="Description" 
        type="textarea"
      />
    </form>
  </div>
</template>

<script>
import axios from "axios";
import InputModule from "@/components/input/Input.vue";
import Form from "@/components/Form.vue";

export default {
  name: "SocietyEdit",
  components: {
    InputModule,
    Form
  },
  props: {
    socID: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      name: "",
      description: "",
    };
  },
  mounted(){
    if (!this.socID) {
      this.$router.push({name:'selectSociety'})
    }
    this.getEventInfo()
  },
  methods: {
    getEventInfo() {
      this.$store.commit("loading", true);
      axios
        .get('/api/society', {
          params: {
            societyID: this.socID
          }
        })
        .then(response => {
          const data = response.data.data;
          this.name = data.name;
          this.description = data.description;
        })
        .catch(c => console.log(c))
        .finally(() => this.$store.commit("loading", false));
    },
    submitEventForm() {
      const data = {
        name: this.name,
        description: this.description,
      };
      axios({
        url: "/api/society",
        data: data,
        method: 'PATCH',
        params: {
          societyID: this.socID,
        },
      }).then(() => {
        this.$router.push({
          name: "society",
          params: { socID: this.socID }
        });
      })
        .catch(error => {
                    console.log(error.response); //eslint-disable-line
        });
    }
  }
};
</script>

<style scoped>
textarea {
    max-width: 20rem;
}
</style>
