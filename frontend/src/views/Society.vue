<template>
    <!--- TODO: style this lmao -->
    <div class="wrapper">

        <SelectSociety v-if="!socID"/>
        <div v-else-if="isStaff">
            <h2>Society page for {{ socName }} </h2>
            <MakeAdmin :socID="socID"/>
        </div>
    </div>
</template>

<script>
import MakeAdmin from "@/components/MakeAdmin.vue";
import SelectSociety from "@/components/SelectSociety.vue";
import { mapGetters } from 'vuex'

export default {
  name: 'EventSign',
  props: {
    socID: {
      type: String
    }
  },
  components: {
    MakeAdmin, SelectSociety
  },
  computed: {
    ...mapGetters('user', [
    'staffSocieties', 'allSocieties'
    ]),
    isStaff() {
        return this.staffSocieties.some(e => e.societyID === this.socID)
    },
    socName() {
        return this.allSocieties.find(e => {
            return e.societyID === this.socID
        }).societyName
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