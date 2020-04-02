<template>
    <div class="wrapper">
        <SelectSociety v-if="!socID"/>
        <div v-else>

            <h2 v-once>Society page for {{ socName }} </h2>
            <img :src="`${apiURL}/api/soc/image?socID=${socID}`" />
            <EventList
              :eventViewTitle="'Upcoming Events for ' + socName"
              :eventData="societyEvents"
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
import { apiURL } from '@/util'

export default {
  name: 'Society',
  props: {
    socID: {
      type: String
    }
  },
  data() {
    return {
      apiURL
    }
  },
  components: {
    MakeAdmin, SelectSociety, EventList
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
  async mounted() {
    
  }
}
</script>

<style>
.wrapper {
    margin: auto;
    width: 80%;
}

</style>