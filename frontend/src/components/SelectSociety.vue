<template>
    <div class="container">
        
        <div   class="form-container">
            <div class="form">

                <h2>Choose your society</h2>
                <select class="input--select select--admin"  v-model="selectedSociety" name="society-select">
                <option value="" >Select a society</option>
                <option
                    v-for="(society, index) in joinedSocieties"
                    :key="index"
                    :value="society.societyID"
                >{{ society.societyName }}{{ isStaff(society.societyID) ? ' (Admin)' : null}}</option>
                </select>
                <button @click="selectSociety" class="btn btn-primary">Next</button>
            </div>
        </div>
        <div class="event-view-title">
          <h3 class="event-view-title-text" v-once>Societies</h3>
          <!-- <a class="event-view-more link" @click="viewAllData = !viewAllData"
            >View {{viewAllData ? 'less' : 'more'}}</a> -->
        </div>

        <Loader v-if="loading"/>
        <FormError v-else-if="societies.length === 0" msg="Seems like there is no events at the moment"/> 
        <div v-else class="event-cards " >
          <Card v-for="(society, index) in cardData" :key="index" :data="society" />
        </div>
    </div>
</template>
<script>
import Card from '@/components/EventCard.vue'
import FormError from '@/components/FormError.vue'
import Loader from '@/components/Loader.vue'
import { mapGetters } from 'vuex'
import axios from 'axios'
export default {
    name: "SelectSociety",
    components: {
        Card, FormError, Loader
    },
    data() {
        return {
            loading: false,
            societies: [],
            selectedSociety: ''
        }
    },
    computed: {
        ...mapGetters('user', [
        'joinedSocieties', 'staffSocieties'
        ]),
        cardData() {
            console.log( this.societies.map(s => ({
                title: s.societyName,
                _link: `/society/${s.societyID}`
            })))
            return this.societies.map(s => ({
                title: s.societyName,
                _link: `/society/${s.societyID}`
            }))
        }
    },
    mounted() {
        this.loading = true
        axios({
            url:'api/soc/getAllSocs'
        }).then(r => {
            this.societies = r.data
            console.log(r)
        }).finally(() => this.loading = false)
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
<style scoped>

.event-view-title{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.event-cards {

  flex-wrap: wrap;
  margin: 0 1rem ;
  /* box-shadow: inset 0 0 2rem 0 rgba(59,59,95,.3);
  border-radius: 5px; */
  padding: 1rem 1rem 1.25rem 1rem;
  /* background: #e3f2fd; */
  display: flex;
}
</style>