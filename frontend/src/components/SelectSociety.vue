<template>
    
    <div   class="form-container">
        <div class="form">

            <h2>Choose your society</h2>
            <select class="input--select select--admin"  v-model="selectedSociety" name="society-select">
            <option value="" >Select a society</option>
            <option
                v-for="(society, index) in allSocieties"
                :key="index"
                :value="society.societyID"
            >{{ society.societyName }}{{ isStaff(society.societyID) ? ' (Admin)' : null}}</option>
            </select>
            <button @click="selectSociety" class="btn btn-primary">Next</button>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    name: "SelectSociety",
    data() {
        return {
            selectedSociety: ''
        }
    },
    computed: {
        ...mapGetters('user', [
        'allSocieties', 'staffSocieties'
        ]),
    },
    methods: {
        selectSociety() {
            this.$router.push({ name: "society", params: { socID: this.selectedSociety } });
        },
        isStaff(socID) {
            return this.staffSocieties.some(e => e.societyID === socID)
        }
    }
}
</script>