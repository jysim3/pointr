<template>
    
    <div>
        <form @submit="submitForm">
        <input type="text" v-model="zid"/>
        <input type="submit"/>
        </form>
    </div>
</template>
<script>
export default {
    name: "hi",
    data() {
        return {
            zid: ''
        }
    },
    methods: {
        submitForm(e) {
            e.preventDefault();
        }
    }
}
</script>
<style scoped>

</style>