<template>

    <div>
        <SelectSociety  v-if="!socID"/>
        <Loader v-else-if="loading" />
        <SocietyPage :socID="socID" v-else />
    </div>
</template>



<script>
import SocietyPage from "@/components/SocietyPage.vue";
import SelectSociety from "@/components/SelectSociety.vue";
import Loader from "@/components/Loader.vue";
import { mapGetters } from 'vuex'

export default {
  name: 'Society',
  props: {
    socID: {
      type: String
    }
  },
  components: {
    SelectSociety, Loader,
    SocietyPage
    
  },
  data() {
    return {
      loading: false,
    }
  },
  computed: {
    ...mapGetters('user', [
    'staffSocieties', 'joinedSocieties', 'allSocietyEvents'
    ]),
    isStaff() {
        return this.staffSocieties.some(e => e.societyID === this.socID)
    },
    societyEvents() {
      return this.allSocietyEvents(this.socID)
    }
  },
}
</script>