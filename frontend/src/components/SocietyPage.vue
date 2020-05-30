<template>
    <div v-if="status === 'success'">
        <div class="container header">
            <div class="profile">
                <div class="profile-info">
                    <h2 class="profile-info-title" >{{ socData.name }}</h2>
                    <i class="material-icons profile-info-button">favorite</i>
                    <!-- TODO: MAKE THIS 'JOIN SOCIETY' -->
                    <p>{{ socData.description }}</p>
                </div>
                <img v-if="socData" :src="apiURL + socData.logo" />
            </div>
            <div class="profile-buttons">
                <i class="material-icons profile-buttons-followers">person</i>
                <span class="profile-buttons-followers">{{ socData.membersCount}} members</span>
                <!-- <i class="material-icons profile-buttons-followers" style="color: purple">trending_up</i>
                <span class="profile-buttons-followers">150 weekly active users</span>-->
            </div>
        </div>

        <div class="container">
            <div class="tabs-wrapper">
                <ul class="tabs">
                    <li class="tabs-item tabs-item--active">Home</li>
                    <li class="tabs-item">TBC</li>
                    <li class="tabs-item">TBC</li>
                    <li class="tabs-item">TBC</li>
                </ul>
            </div>
        </div>

        <div class="main">
            <div class="container">
                <EventList
                    :eventViewTitle="'Upcoming Events for ' + socData.name"
                    :eventData="societyEvents"
                    listStyle="table"
                />
                <EventList
                    :eventViewTitle="'Past Events for ' + socData.name"
                    :eventData="pastSocietyEvents"
                    listStyle="table"
                    :loading="pastEventsLoading"
                />
                <MakeAdmin v-if="isStaff" :socID="socID" />
                <!--- TODO: more features for admins-->
            </div>
        </div>
    </div>
</template>
<script>
import EventList from "@/components/EventList.vue";
import MakeAdmin from "@/components/MakeAdmin.vue";
import axios from "axios";
import { mapGetters } from "vuex";

export default {
    components: {
        MakeAdmin,
        EventList
    },
    props: ["socID"],
    data() {
        return {
            pastSocietyEvents: [],
            societyEvents: [],
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
            apiURL: require("@/util").apiURL
        };
    },
    created() {
        if (this.status === null) {
            this.updateSocietyData();
        }
    },
    computed: {
        ...mapGetters("user", [
            "staffSocieties",
        ]),
        isStaff() {
            return this.staffSocieties.some(e => e.societyID === this.socID);
        },
    },
    methods: {
        updateSocietyData() {
            if (!this.socID) {
                return;
            }
            this.loading = true;
            this.$store.commit("loading", true);
            axios
                .get(`/api/society`, {
                    params: {
                        societyID: this.socID
                    }
                })
                .then(v => {
                    const data = v.data.data;
                    Object.assign(this.socData,data)
                    this.status = v.data.status
                })
                .catch(e => {
                    console.log(e); // eslint-disable-line
                })
                .finally(() => this.$store.commit("loading", false));

            this.pastEventsLoading = true;
            axios
                .get(`/api/society/events/past`, {
                    params: {
                        societyID: this.socID
                    }
                })
                .then(v => {
                    this.pastSocietyEvents = v.data.data;
                })
                .catch(e => {
                    console.log(e); // eslint-disable-line
                })
                .finally(() => (this.pastEventsLoading = false));
        }
    }
};
</script>
<style scoped>
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
    cursor: pointer;
}
.profile > img {
    width: 150px;
    object-fit: cover;
    height: 150px;
    box-shadow: 0 0rem 2rem 0rem rgba(59, 59, 95, 0.3);
    border-radius: 150px;
    margin: 0 3rem 2rem 3rem;
    flex-shrink: 0;
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
    left: 0;
    position: absolute;
    background: white;
    padding: 0 3rem;
}
@media only screen and (max-width: 700px) {
    .profile {
        flex-direction: column-reverse;
        text-align: center;
    }
}
</style>