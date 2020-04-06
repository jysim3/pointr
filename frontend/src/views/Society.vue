<template>
    <div class="wrapper">
        <SelectSociety v-if="!socID"/>
        <div v-else>

            <div class="header">
              <!-- <h1 class="header-text" v-once>{{ socName }}</h1> -->
              <img v-if="socData" :src="apiURL + socData.logo" />
            </div>

            <EventList
              :eventViewTitle="'Upcoming Events for ' + socName"
              :eventData="societyEvents"
              listStyle="table"
            />
            <EventList
              :eventViewTitle="'Past Events for ' + socName"
              :eventData="pastSocietyEvents"
              listStyle="table"
              :loading="pastEventsLoading"
            />
            <MakeAdmin v-if="isStaff" :socID="socID"/>
            <!--- TODO: more features for admins-->


        </div>
    </div>
</template>

<style>
.wrapper {
    margin: auto;
    width: 80%;
}
.header {
  text-align: center;
}
.header h1 {
  font-size: 4rem;
}
.header > img {
  max-width: 100%;
  border-radius: 10px ;
  box-shadow:   0 0rem 2rem 0rem rgba(59,59,95,0.3);
  border-radius: 10px ;
}

</style>

<script>
import MakeAdmin from "@/components/MakeAdmin.vue";
import SelectSociety from "@/components/SelectSociety.vue";
import EventList from "@/components/EventList.vue";
import { mapGetters } from 'vuex'
import { fetchAPI } from '@/util.js'

export default {
  name: 'Society',
  props: {
    socID: {
      type: String
    }
  },
  components: {
    MakeAdmin, SelectSociety, EventList
  },
  data() {
    return {
      pastSocietyEvents:[
      ],
      pastEventsLoading: false,
      socData: {},
      apiURL: require('@/util').apiURL
    }
  },
  watch: {
    socID: function() {
      this.loading = true
      this.$nextTick(() => this.updateSocietyData())
    }
  },
  created() {
    this.updateSocietyData()
  },
  computed: {
    ...mapGetters('user', [
    'staffSocieties', 'joinedSocieties', 'allSocietyEvents'
    ]),
    isStaff() {
        return this.staffSocieties.some(e => e.societyID === this.socID)
    },
    socName() {
        return this.joinedSocieties.find(e => {
            return e.societyID === this.socID
        }).societyName
    },
    societyEvents() {
      return this.allSocietyEvents(this.socID)
    }
  },
  methods: {
    updateSocietyData() {
      if (!this.socID) {
        return
      }
      fetchAPI(`/api/soc?socID=${this.socID}`, "GET")
      .then(v => {
        this.socData = v.data
        console.log(v.data) // eslint-disable-line
        this.loading = true
      })
      .catch(e => {
        console.log(e) // eslint-disable-line
      })
      this.pastEventsLoading = true
      fetchAPI(`/api/soc/getPastEvents?socID=${this.socID}`, "GET")
      .then(v => {
        this.pastSocietyEvents = v.data
        this.pastEventsLoading = false
      })
      .catch(e => {
        console.log(e) // eslint-disable-line
      })
    }
  }
}
</script>