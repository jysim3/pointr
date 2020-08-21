<template>
  <div>
    <!-- TODO: LET USER EDIT THIS INFO -->
    <Loader v-if="loading" />
    <div v-else>
      <div class="wrapper header">
        <div class="profile">
          <div class="profile-info">
            <!-- <div class="profile-info-group">
                        <span class="profile-info-numbers">50</span>
                        <span class="profile-info-subtitle">followers</span>
                    </div>
                    <div class="profile-info-group">
                        <span class="profile-info-numbers">10</span>
                        <span class="profile-info-subtitle">events went</span>
                    </div> -->
          </div>
          <!-- TODO: Let user modify -->
          <ProfilePhoto
            v-if="userData"
            class="profile-photo"
            :src="userImage"
          />
          <!-- <div class="profile-buttons">
                    <i class="material-icons profile-info-button">favorite</i>
                    </div> -->
        </div>
      </div>
            





      <div class="main wrapper">
        <div class="main-name">
          <h2
            v-once
            class="main-name-title"
          >
            {{ userData.firstname }} {{ userData.lastname }}
          </h2>
          <span
            v-once
            class="main-name-subtitle"
          >{{ userData.zID }}</span>
        </div>

        <p class="main-description">
          {{ userData.description }}
        </p>
        <div
          v-for="(s,i) in stats"
          :key="i"
          class="main-stats"
        >
          <i class="material-icons">{{ s.icon }}</i>
          <span>{{ s.text }}</span>
        </div>
        <EventList
          event-view-title="Attended events"
          :event-data="eventData"
        >
          <template #action>
            <span/>
          </template>
        </EventList>

        <!--- TODO: more features for admins-->
      </div>
    </div>
  </div>
</template>


<script>
import ProfilePhoto from "@/components/ProfilePhoto"
import Loader from "@/components/Loader.vue";
import EventList from "@/components/EventList.vue";
import axios from 'axios'

export default {
  name: 'User',
  components: {
    Loader,
    ProfilePhoto,
    EventList
  },
  props: {
    zID: {
      type: String
    }
  },
  data() {
    return {
      userData: {},
      eventData: {},
      apiURL: require('@/util').apiURL,
      loading: false,
      statsData: [
      ]
    }
  },
  computed: {
    userImage() {
      if (this.userData.image) {
        return this.apiURL + this.userData.image
      }
      return ""
    },
    stats () {
      const stat = this.statsData
      if (this.userData.societies > 0) {
        stat.push(
          {
            icon: 'home',
            text: 'Admin for ' + this.userData.societies.staff.map(v => v.societyName).join(', ')
          })
      }
      return stat
    }
  },
  watch: {
    zID: function() {
      this.loading = true
      this.$nextTick(() => this.updateUserData())
    }
  },
  created() {
    this.updateUserData()
  },
  methods: {
    updateUserData() {
      if (!this.zID) {
        return
      }
      this.loading = true
      axios.get(`/api/user/events/past?zID=${this.zID}`)
        .then(v => {
          const data = v.data.data
          this.eventData = data
        })
      axios.get(`/api/user?zID=${this.zID}`)
        .then(v => {
          const data = v.data.data
          this.userData.firstname = data.firstname
          this.userData.lastname = data.lastname
          this.userData.image = data.image
          this.userData.societies = data.societies
          this.userData.description = data.description
          // this.userData.events = data.events

          this.loading = false
        })
        .catch(e => {
        console.log(e) // eslint-disable-line
        })
    }
  }
}
</script>
<style scoped>
.wrapper {
    margin: auto;
    width: 80%;
    max-width: 900px;
}
.header {
  margin-top: 20%;
  position: relative;
}
.profile {
  display: flex;
  align-items: center;
  justify-content: space-between;
    position: relative;
}
.profile > * {
    flex: 0 0 0;
}
.profile-info {
    display: flex;
}
.profile-info-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-right: 1.5rem;
    width: 90px;
}
.profile-info-numbers {
    font-size: 1.5rem;
    color: black;
}
.profile-info-subtitle {
    padding-top: 0.5rem;
}
.profile-photo {
  width: 150px;
  object-fit: cover;
  height: 150px;
  box-shadow:   0 0rem 2rem 0rem rgba(59,59,95,0.3);
  border-radius: 150px ;
  position: absolute;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  z-index: 1;
  margin: auto;
}
.tabs-wrapper, .tabs {
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
  border-radius: 5px 5px 0 0 ;
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
  background: white;
  padding: 3rem;
  padding-top: 150px;
  margin-top: -75px;
  z-index: -1;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.main > * {
    text-align: center;
    width: 80%;
}
.main-name {
    padding-bottom: 2rem;
    color: black;
}
.main-description {
    font-size: 0.9rem;
}
.main-stats {
    padding-top: 2rem;
}
.main-stats i {
    margin-right: 1rem;
}
.main-stats * {
  vertical-align: middle;
}
@media only screen and (max-width: 700px) {
  .profile {
    flex-direction: column-reverse;
    text-align: center;
  }
}
</style>