<template>
    <div>
        <div class="form-container">
            <form id="create-event-form" class="form" @submit.prevent="submitEventForm">
                <div class="form-back-link">
                <router-link :to="{name:'society',params: {socID}}" class="material-icons primary">chevron_left</router-link>
                </div>
                <h2>Edit society Details</h2>

                <InputModule required 
                name="name" 
                label="Society Name" 
                type="input" 
                v-model="name" />

                <InputModule required 
                name="description" 
                label="Description" 
                type="textarea" 
                v-model="description" />

                <button type="submit" class="btn btn-primary">Edit Society</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import InputModule from "@/components/input/Input.vue";

export default {
    name: "SocietyEdit",
    props: {
        socID: {
            type: String,
            default: null
        }
    },
    components: {
        InputModule
    },
    data() {
        return {
            name: "",
            description: "",
        };
    },
    mounted(){
        if (!this.socID) {
            this.$router.push({name:'selectSociety'})
        }
        this.getEventInfo()
    },
    methods: {
        getEventInfo() {
            this.$store.commit("loading", true);
            axios
                .get('/api/society', {
                    params: {
                        societyID: this.socID
                    }
                })
                .then(response => {
                    const data = response.data.data;
                    this.name = data.name;
                    this.description = data.description;
                })
                .catch(c => console.log(c))
                .finally(() => this.$store.commit("loading", false));
        },
        submitEventForm() {
            const data = {
                name: this.name,
                description: this.description,
            };
            axios({
                url: "/api/society",
                data: data,
                method: 'PATCH',
                params: {
                    societyID: this.socID,
                },
            }).then(() => {
                    this.$router.push({
                        name: "society",
                        params: { socID: this.socID }
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
