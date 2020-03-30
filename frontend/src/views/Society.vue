<template>
    <!--- TODO: style this lmao -->
    <div class="wrapper">
        <SelectSociety v-if="!socID"/>
        <div v-else>

            <h2 v-once>Society page for {{ socName }} </h2>

            <EventList
              :eventViewTitle="'Upcoming Events for ' + socName"
              :eventData="societyEvents"
              listStyle="table"
            />



            <MakeAdmin v-if="isStaff" :socID="socID"/>


        </div>
    </div>
</template>

<script>
import MakeAdmin from "@/components/MakeAdmin.vue";
import SelectSociety from "@/components/SelectSociety.vue";
import EventList from "@/components/EventList.vue";
import { mapGetters } from 'vuex'

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
  computed: {
    ...mapGetters('user', [
    'staffSocieties', 'allSocieties', 'allSocietyEvents'
    ]),
    isStaff() {
        return this.staffSocieties.some(e => e.societyID === this.socID)
    },
    socName() {
        return this.allSocieties.find(e => {
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