<template>
  <div class="form-container" id="join-society-form-container">
    <form @submit.prevent="submitJoinSocietyForm" class="form">
      <h2>Join a society</h2>
      <FormError v-if="error" :msg="error" />
      <label for="society" class="label">Choose a society</label>
      <!-- TODO: This would need to become searchable in the future.  -->
      <!-- TODO: what if there are no availableSocieties -->
      <select v-model="selectedSociety" class="input--select" name="society-select">
        <option
          v-for="(society, index) in availableSocieties"
          :key="index"
          :value="society"
        >{{ society.societyName }}</option>
      </select>
      <button type="submit" class="btn btn-primary">Join</button>
      <h3 id="msg--success" v-show="success">Success!</h3>
    </form>
  </div>
</template>

<script>
import { fetchAPI } from "@/util";
import { mapGetters } from 'vuex';
import FormError from "@/components/FormError.vue";

export default {
  name: "SocietyJoin",
  components: {
    FormError
  },
  data() {
    return {
      selectedSociety: "",
      allSocietiesData: [],
      success: false,
      error: ""
    };
  },
  computed: {
    ...mapGetters('user', [
      'joinedSocieties'
    ]),
    availableSocieties() {
      return this.allSocietiesData.filter(s => !this.joinedSocieties.includes(s))
    }
  },
  async created() {
    const response = await fetchAPI("/api/soc/getAllSocs", "GET");
    this.allSocietiesData = response.data;
  },
  methods: {
    async submitJoinSocietyForm() {
      try {
        this.success = false
        await fetchAPI(`/api/soc/join`, "POST", {
          societyID: this.selectedSociety.societyID
        })
        this.error = ""
        this.success = true
      } catch (error) {
        if (error.response.status === 403) {
          this.error = `You're already a part of this society`;
        } else {
          this.error = `There was an error while trying to join ${this.selectedSociety.societyName}`;
        }
      }
    }
  }
};
</script>

<style scoped>
#msg--success {
  margin-top: 2rem;
}
</style>