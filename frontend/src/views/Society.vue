<template>
    <div class="wrapper">
        <SelectSociety v-if="!socID"/>
        <div v-else>

            <h2 v-once>Society page for {{ socName }} </h2>

            <EventList
              :eventViewTitle="'Upcoming Events for ' + socName"
              :eventData="societyEvents"
              listStyle="table"
            />
            <EventList
              :eventViewTitle="'Past Events for ' + socName"
              :eventData="pastSocietyEvents"
              listStyle="table"
            />
            <MakeAdmin v-if="isStaff" :socID="socID"/>
            <!--- TODO: more features for admins-->


        </div>
    </div>
</template>

<script>
import MakeAdmin from "@/components/MakeAdmin.vue";
import SelectSociety from "@/components/SelectSociety.vue";
import EventList from "@/components/EventList.vue";
import { mapGetters } from 'vuex'
import { fetchAPI } from '@/util.js'

export default {
  name: 'EventSign',
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
      ]
    }
  },
  mounted() {
      fetchAPI(`/api/soc/getPastEvents?socID=${this.socID}`, "GET")
      .then(v => {
        this.pastSocietyEvents = v.data
      })
      .catch(e => {
        console.log(e) // eslint-disable-line
      })
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
  }
}
</script>

<style>
.wrapper {
    margin: auto;
    width: 80%;
}

</style>