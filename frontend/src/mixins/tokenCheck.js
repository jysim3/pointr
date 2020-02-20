// import router from "@/router/index.js"
import { getToken } from "@/util.js";

export default {
    data() {
        return {
            token: ""
        }
    },
    created() {
        // TODO: also need to check that token is actually valid.
        const localStorageToken = getToken()
        if (!localStorageToken) {
            console.log('NO TOKEN FOUND') //eslint-disable-line
            // router.push({ name: "signIn" }) //TODO: redirect is bad UX because can't go back!
        } else {
            this.token = localStorageToken
        }
    }
}