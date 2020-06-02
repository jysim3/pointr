<template>
    <div class="form-container" id="form-container--signin">
        <form @submit.prevent="submitRequest" class="form">
            <h2>Request</h2>
            <FormError v-if="error" :msg="error" />
            <InputModule required v-model="title" label="Title" />
            <!-- <div class="label-input-div">
        <label class="label input--checkbox-label">Remember me</label>
        <input v-model="rememberUser" class="input input--checkbox" type="checkbox" />
            </div>-->
            <InputModule
                required
                label="Contact reason"
                type="select"
                :options="availableRequest"
                v-model="requestSelection"
            />

            <InputModule label="Society Name (optional)" v-model="societyName"/>

            <InputModule required label="Message" v-model="message" type="textarea"/>

            <button v-if="status === ''" type="submit" class="btn btn-primary">Request</button>
            <h3 v-else> Success! </h3>
        </form>
    </div>
</template>

<script>
import InputModule from "@/components/input/Input.vue";
import axios from "axios"
export default {
    name: "RequestForm",
    props: {
        request: {
            type:String,
            default: ''
        }

    },
    components: {
        InputModule
    },
    data() {
        return {
            title: "",
            error: "",
            requestSelection: this.request,
            availableRequest: [
                { label: "Add my society", value: "addSoc" },
                { label: "I'm not an admin to my society", value: "addAdmin" },
                { label: "There's a bug to ours site", value: "bug" },
                { label: "I want to add/change something", value: "changeRequest/feature" },
                { label: "Complaint", value: "haters" },
                { label: "Others", value: "other" },
                { label: "Just want to make friends", value: "lovers" }
            ],
            message: "",
            societyName: "",
            status: ""
        };
    },
    methods: {
        submitRequest() {

            axios.post('/api/other/enquire',{
                message: JSON.stringify({
                    title: this.title,
                    requestSelection: this.requestSelection,
                    societyName: this.societyName,
                    message: this.message
                })
            })
            .then(() => {
                this.status = 'success'
            })
        }
    }
};
</script>

<style scoped>
h3 {
    display: block;
    margin: 1rem auto;
    
}
</style>