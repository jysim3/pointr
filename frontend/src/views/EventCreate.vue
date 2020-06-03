<template>
    <div>
        <div class="form-container">
            <form id="create-event-form" class="form" @submit.prevent="submitEventForm">
                <div class="form-back-link">
                <router-link :to="{name:'event',params: {eventID}}" class="material-icons primary">chevron_left</router-link>
                </div>
                <h2>{{ this.eventID ? 'Edit' : 'Create an'}} event</h2>

                <InputModule required label="Event title" type="input" v-model="name" />

                <InputModule required label="Location" type="input" v-model="location" />

                <InputModule required label="Description" type="textarea" v-model="description" />

                <InputModule
                    required
                    label="Society"
                    type="select"
                    :options="availableSocieties"
                    v-model="society"
                />

                <InputModule required label="Start Date" type="date" v-model="startDate" @input="updateDate(startDate)"/>

                <InputModule required label="Start Time" type="time" v-model="startTime" />

                <InputModule required label="Start Date" type="date" v-model="endDate" />

                <InputModule required label="End Time" type="time" v-model="endTime" />

                <!-- <label class="label" for>Set default points</label>
        <input class="input" v-model="point" type="number" min="0" required />
        <label class="label" for>Show QR Code/Event link</label>
                <input class="input" type="checkbox" checked />-->
                <button type="submit" class="btn btn-primary">{{ eventID ? 'Edit' : 'Create' }} Event</button>
                <button type="button" class="btn btn-warning"
                v-if="eventID" @click="deleteEvent" @focusout="deleteConfirmation = 0"
                >
                    {{ deleteConfirmation === 0 ? 'Delete Event' : 'Are you sure?' }}
                </button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import InputModule from "@/components/input/Input.vue";

export default {
    name: "EventCreate",
    props: {
        eventID: {
            type: String,
            default: null
        }
    },
    components: {
        InputModule
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
            availableSocieties: this.$store.getters[
                "user/societies"
            ].admins.map(s => ({
                value: s.id,
                label: s.name
            }))
        };
    },
    mounted(){
        this.getEventInfo()
    },
    methods: {
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
            axios
                .get(`/api/event?eventID=${this.eventID}`)
                .then(response => {
                    const data = response.data.data;
                    this.name = data.name;
                    this.location = data.location;
                    this.society = data.society[0].id;
                    this.description = data.description;
                    this.startTime = data.start.split(' ')[1].split(':').slice(0,2).join(':')
                    this.startDate = data.start.substr(0,10)
                    this.endTime = data.end.split(' ')[1].split(':').slice(0,2).join(':')
                    this.endDate = data.start.substr(0,10)
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
                tags: [0],
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
            }).then(response => {
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

<style scoped>
textarea {
    max-width: 20rem;
}
</style>
