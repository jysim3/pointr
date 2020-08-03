<template>
  <div
    v-if="status === 'success'"
    class="society-page"
  >
    <div class="container header">
      <div class="profile">
        <div class="profile-info">
          <h2 class="profile-info-title">
            {{ socData.name }}
          </h2>
          <button
            v-if="!isSocietyAdmin"
            class="btn btn-primary profile-info-button"
            @click="joinSociety"
          >
            {{ !isSocietyMember ? 'Join' : 'Leave' }}
          </button>
          <button
            v-else
            class="btn btn-warning profile-info-button"
          >
            Admin
          </button>
          <!-- TODO: MAKE THIS 'JOIN SOCIETY' -->
          <p>{{ socData.description }}</p>
        </div>
        <ProfilePhoto
          v-if="socData" 
          :update-u-r-l="isSocietyAdmin ? `/api/society/logo?societyID=${socID}` : null"
          :src="apiURL + socData.photo" 
          @update="updateSocietyData"
        />
      </div>
      <div class="profile-buttons">
        <i class="material-icons profile-buttons-followers">person</i>
        <span class="profile-buttons-followers">{{ members }} members</span>
        <!-- <i class="material-icons profile-buttons-followers" style="color: purple">trending_up</i>
                <span class="profile-buttons-followers">150 weekly active users</span>-->
      </div>
    </div>

    <div class="container">
      <div class="tabs-wrapper">
        <ul class="tabs">
          <li
            v-for="(text, index) in tabs"
            :key="index"
            :class="['tabs-item', {'tabs-item--active':activeTab==index}]"
            @click="changeTab(index)"
          >
            {{ text }}
          </li>
        </ul>
      </div>
    </div>
    <div class="container-fluid main">
      <div class="continaer">
        <SocietyEvents
          v-if="activeTab == 0"
          :soc-i-d="socID"
          :soc-data="socData"
        />
        <div v-if="activeTab == 1"> 
          <SocietyAdmin 
            :soc-i-d="socID"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import SocietyEvents from "@/components/SocietyEvents.vue";
import SocietyAdmin from "@/components/SocietyAdmin.vue";
import ProfilePhoto from '@/components/ProfilePhoto.vue'
import axios from "axios";

export default {
  components: {
    SocietyAdmin,
    SocietyEvents,
    ProfilePhoto
  },
  props: {
    socID: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      pastEventsLoading: false,
      status: null,
      socData: {
        description: "",
        id: "",
        name: "",
        photo: null,
        previewDescription: null,
        tags: null,
        type: 0,
      },
      tabs: ['Events','Admin Tools'],
      activeTab: 0,
      members: 0,
      apiURL: require("@/util").apiURL,
      isSocietyMember: this.$store.getters['user/isSocietyMember'](this.socID), 
    };
  },
  computed: {
    isSocietyAdmin() { return this.$store.getters['user/isSocietyAdmin'](this.socID) },
  },
  created() {
    if (this.status === null) {
      this.updateSocietyData();
    }
  },
  methods: {
    changeTab(index) {
      this.activeTab = index
    },
    joinSociety() {
      axios({
        url: !this.isSocietyMember?'/api/society/join': '/api/society/leave',
        method: "POST",
        params:{
          societyID: this.socID
        }
      }).then(() => {
        this.isSocietyMember = !this.isSocietyMember
        if (this.isSocietyMember) {
          this.members++
        } else {
          this.members--
        }
      })
    },
    updateSocietyData() {
      if (!this.socID) {
        return;
      }
      this.loading = true;
      this.$store.commit("loading", true);
      const urls = [
        '/api/society',
        '/api/society/members'
      ]
      Promise.all(urls.map(u => axios.get(u,{
        params: {
          societyID: this.socID
        }
      })))
        .then(([socData, members]) => {
          Object.assign(this.socData,socData.data.data)
          this.members = members.data.data
          this.status = 'success'
          document.title = `${this.socData.name} - Pointr`

        }).catch(c => {
          console.log(c)
          this.$router.push({name:'404'})
        }).finally(() => this.$store.commit("loading", false));
    }
  }
};
</script>
<style scoped>
.society-page {
    display: flex;
    flex-direction: column;
}
.header {
    margin-top: 4rem;
}
.profile {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.profile-info > h2 {
    font-size: 2rem;
    color: black;
}
.profile-info > i {
    margin-left: 1rem;
    color: red;
}
.profile-info > i,
h2 {
    display: inline;
    vertical-align: middle;
}
.profile-info > p {
    padding-top: 1rem;
}
.profile-info-button {
    margin-left: 1rem;
    cursor: pointer;
}
span.profile-buttons-followers {
    margin-right: 1rem;
}
.profile-buttons-followers {
    vertical-align: middle;
}
.tabs-wrapper,
.tabs {
    width: 100%;
}
.tabs-wrapper {
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
.tabs {
    list-style-type: none;
    margin-bottom: -1px;
    display: flex;
    margin-top: 3rem;
    padding: 0;
}
.tabs-item {
    display: block;
    flex: 1 1 0;
    text-align: center;
    margin-right: 2px;
    padding: 0.5rem 1rem;
    border-radius: 5px 5px 0 0;
    background-color: #e3f2fd;
    color: black;
    max-width: 8rem;
    cursor: pointer;
}
.tabs-item--active {
    background-color: white;
}
.tabs-item:hover {
    background-color: var(--c-primary);
}

.main {
    width: 100%;
}
@media only screen and (max-width: 700px) {
    .profile {
        flex-direction: column-reverse;
        text-align: center;
    }
    .profile-buttons {
        padding-top: 1rem;
        display: flex;
        justify-content: center;
    }
}
.box {
    margin: 2rem;
    max-width: 200px;
}
</style>