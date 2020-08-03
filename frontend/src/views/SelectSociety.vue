<template>
  <div class="container">
    <CardContainer title="Your Societies">
      <template #options>
        <p>
          Your society is not here? Request it 
          <router-link :to="{name:'request', params: {request:'addSoc'}}">
            here
          </router-link>
        </p>
      </template>
      <Card
        v-for="(society, index) in userSocietyData"
        :key="index"
        :data="society"
      />
    </CardContainer>
    <CardContainer
      title="Browse Societies"
      :loading="loading"
      :error="error"
    >
      <Card
        v-for="(society, index) in allSocietyData"
        :key="index"
        :data="society"
      />
    </CardContainer>
  </div>
</template>
<script>
import Card from '@/components/EventCard.vue'
import CardContainer from '@/components/CardContainer.vue'
import axios from 'axios'
export default {
  name: "SelectSociety",
  components: {
    Card, CardContainer
  },
  data() {
    return {
      loading: false,
      societies: [],
      selectedSociety: '',
      error: ''
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
    }).catch(() => {
      this.error = "Seems like there is no society at the moment"
    }).finally(() => this.loading = false)
  },
  methods: {
    isStaff(socID) { return this.$store.getters['user/isSocietyAdmin'](socID)}
  }
}
</script>