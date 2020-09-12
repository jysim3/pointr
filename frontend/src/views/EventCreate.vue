<template>
  <div class="container">
    <Form
      :back-link="eventID ? {name:'event',params: {eventID}} : null"
      @submit="submitEventForm"
    >
      <template #header>
        <h2>{{ eventID ? 'Edit' : 'Create an' }} event</h2>
      </template>

      <InputModule
        v-model="name"
        required
        name="title"
        label="Event title"
        type="input"
      />

      <InputModule
        v-model="location"
        required
        name="location"
        label="Location"
        type="input"
      />

      <InputModule
        v-model="description"
        required
        name="description"
        label="Description"
        type="textarea"
      />

      <InputModule
        v-model="society"
        required
        label="Society"
        type="select"
        :options="availableSocieties"
      />

      <InputModule
        v-model="startDate"
        required
        name="startDate"
        label="Start Date"
        type="date"
        @input="updateDate(startDate)"
      />

      <InputModule
        v-model="startTime"
        required
        name="startTime"
        label="Start Time"
        type="time"
      />

      <InputModule
        v-model="endDate"
        required
        name="startDate"
        label="End Date"
        type="date"
        :min="moment().format('YYYY-MM-DD')"
      />

      <InputModule
        v-model="endTime"
        required
        name="endTime"
        label="End Time"
        type="time"
      />
      <div
        class="form-group d-flex flex-wrap w-100"
      >
        <label class="label">Tags</label>
        <Tagify 
          v-model="tags"
          :settings="{whitelist: availableTags, dropdown: { enabled: 0 }, enforceWhitelist: true }"
        />
      </div>
      <div class="form-group">
        <label> Cover photo </label>
        <div class="custom-file">
          <input type="file" class="custom-file-input" id="inputGroupFile01" @change="onFileSelected" accept="image/png, image/jpeg">
          <label class="custom-file-label">{{ this.file.name || 'Choose cover photo' }}</label>
        </div>
      </div>
      <InputModule
        v-model="privacy"
        name="privacy"
        required
        label="Privacy"
        type="radio"
        :options="privacyOptions"
      />

      <!-- TODO: Clean the photo code up  -->
      <template #footer>
        <div>
          <button
            v-if="eventID"
            type="button"
            class="btn btn-warning"
            @click="deleteEvent"
            @focusout="deleteConfirmation = 0"
          >
            {{ deleteConfirmation === 0 ? 'Delete Event' : 'Are you sure?' }}
          </button>
          <button
            type="submit"
            class="btn btn-primary"
          >
            {{ eventID ? 'Edit' : 'Create' }} Event
          </button>
        </div>
      </template>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import InputModule from "@/components/input/Input.vue";
import Form from "@/components/Form";
import Tagify from '@/components/input/tagify'
import moment from 'moment'

export default {
  name: "EventCreate",
  components: {
    InputModule,
    Form,
    Tagify
  },
  props: {
    eventID: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      deleteConfirmation: 0,
      name: "",
      location: "",
      society: "",
      startDate: "",
      endDate: "",
      description: "",
      startTime: "",
      endTime: "",
      privacy: "",
      tags: [],
      file: {},
      availableTags: this.$store.getters.eventTags.map((v,i)=>({value:v,id:i})),
      availableSocieties: this.$store.getters[
        "user/societies"
      ].admins.map(s => ({
        value: s.id,
        label: s.name
      })),
      privacyOptions: this.$store.getters.privacy.map((v,i)=>({label:v,value:i})),
    }
  },
  mounted(){
    this.getEventInfo()
    if (this.$store.getters.tokenInfo && 
    this.$store.getters.tokenInfo['permission'] === 5){
      axios({
        url:'api/society/all'
      }).then(r => {
        this.availableSocieties = r.data.data.map(s => ({
          value: s.id,
          label: s.name
        }))
      }).catch(() => {
        this.error = "Seems like there is no society at the moment"
      })
    }
  },
  methods: {
    moment: moment,
    onFileSelected(event) {
      const selectedFile = event.target.files[0]
      this.file = selectedFile
    },
    onTagsChange(e) {
      this.tags = e
    },
    updateDate() {
      if (this.endDate === '' || new Date(this.endDate) < new Date(this.startDate)) {
        this.endDate = this.startDate
      }
    },
    deleteEvent() {
      if (this.deleteConfirmation === 0) {
        this.deleteConfirmation = 1
        return
      }
      axios.delete('/api/event',{
        params: {
          eventID: this.eventID
        }
      }).then(() => {
        this.$router.push('/')
      })
    },
    getEventInfo() {
      if (!this.eventID) {
        return;
      }
      this.$store.commit("loading", true);
      axios.get(`/api/event?eventID=${this.eventID}`)
        .then(response => {
          const data = response.data.data;
          this.name = data.name;
          this.location = data.location;
          this.society = data.society[0].id;
          this.description = data.description;
          const start = moment(data.start)
          this.startTime = start.format('HH:mm')
          this.startDate = start.format('YYYY-MM-DD')
          const end = moment(data.end)
          this.endTime = end.format('HH:mm')
          this.endDate = end.format('YYYY-MM-DD')
          this.tags = data.tags.map(t => ({ 
            id: t, 
            value: this.$store.getters.eventTags[t]
          }))
          this.privacy = data.privacy
          console.log(data)
          this.isAdmin = this.$store.getters["user/isSocietyAdmin"](
            data.society
          );
        })
        .catch(c => console.log(c))
        .finally(() => this.$store.commit("loading", false));
    },
    submitEventForm() {
      const data = {
        name: this.name,
        start: new Date(this.startDate + " " + this.startTime),
        end: new Date(this.endDate + " " + this.endTime),
        description: this.description,
        location: this.location,
        status: 0,
        privacy: this.privacy,
        tags: this.tags.map(t => t.id),
        hasQR: true,
        hasAccessCode: false,
        hasAdminSignin: true,
        public: this.publicEvent
      };
      axios({
        url: "/api/event",
        data: data,
        params: {
          societyID: this.society,
          eventID: this.eventID
        },
        method: this.eventID ? 'PATCH' : 'POST'
      }).then(response => new Promise((resolve, reject) => {

        if (response.status == 200) {
          resolve(response.data)
        } else {
          reject(response)
        }
      })).then(response => new Promise((resolve, reject)=> {
        if (!this.file || Object.keys(this.file).length === 0) {
          resolve(response)
        }
        const fd = new FormData;
        fd.append("photo",this.file, this.file.name)
        return axios.post("/api/event/photo", fd, {
          params: {
            eventID: response.data.id
          }
        }).then(photo => {
          if (photo.status == 200) {
            resolve(response)
          } else {
            reject(photo)
          }
        }).catch(e => {
          reject(e)
        })
      })).then( response => {
        console.log(response)
        this.$router.push({
          name: "event",
          params: { eventID: response.data.id }
        });
      })
        .catch(error => {
                    console.log(error.response); //eslint-disable-line
        });
    }
  }
};
</script>

<style >
textarea {
    max-width: 20rem;
}

.tagify {
  width: 100%;
  padding: 0;
  border: 2px solid #dbdbdb;
  transition: all 0.2s;
  border-radius: var(--border-radius);
}
/* TODO: Make box shadows variables */
.tagify:focus {
  border: 2px solid var(--c-secondary-dark);
  box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
  outline: 0;
}
</style>
