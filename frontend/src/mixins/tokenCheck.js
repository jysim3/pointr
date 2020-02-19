// import router from "@/router/index.js"

export default {
    data() {
        return {
            token: ""
        }
    },
    created() {
        const localStorageToken = localStorage.getItem("token")
        if (!localStorageToken) {
            console.log('NO TOKEN FOUND') //eslint-disable-line
            // router.push({ name: "signIn" }) //TODO: redirect is bad UX because can't go back!
        } else {
            this.token = localStorageToken
        }
    }
}