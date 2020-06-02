<template>
    <div class="container">
        
        <div class="event-view-title">
          <h3 class="event-view-title-text">Your Societies</h3>
          <p> Your society is not here? Request it 
              <router-link :to="{name:'request', params: {request:'addSoc'}}"> here </router-link>
          </p>
        </div>
        <div  class="event-cards " >
            <Card v-for="(society, index) in userSocietyData" :key="index" :data="society" />
        </div>

        <h3>Browse Societies</h3>
        <Loader v-if="loading"/>
        <FormError v-else-if="societies.length === 0" msg="Seems like there is no events at the moment"/> 
        <div v-else class="event-cards " >
          <Card v-for="(society, index) in allSocietyData" :key="index" :data="society" />
        </div>
    </div>
</template>
<script>
import Card from '@/components/EventCard.vue'
import FormError from '@/components/FormError.vue'
import Loader from '@/components/Loader.vue'
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
        userSocietyData() {
            return this.societies
            .filter(k => this.$store.getters['user/isSocietyAdmin'](k.id))
            .map(s => ({
                title: s.name,
                subtitle: s.description,
                tags: s.tags,
                _link: `/society/${s.id}`
            }))
        },
        allSocietyData() {
            return this.societies
            .filter(k => !this.$store.getters['user/isSocietyAdmin'](k.id))
            .map(s => ({
                title: s.name,
                subtitle: s.description,
                tags: s.tags,
                _link: `/society/${s.id}`
            }))
        }
    },
    mounted() {
        this.loading = true
        axios({
            url:'api/society/all'
        }).then(r => {
            this.societies = r.data.data
        }).finally(() => this.loading = false)
    },
    methods: {
        selectSociety() {
            this.$router.push({ name: "society", params: { socID: this.selectedSociety } });
        },
        isStaff(socID) { return this.$store.getters['user/isSocietyAdmin'](socID)}
    }
}
</script>
<style scoped>

.event-view-title{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 3rem;
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