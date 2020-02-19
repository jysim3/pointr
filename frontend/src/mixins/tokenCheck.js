import router from "@/router/index.js"
import { getToken } from "@/util.js"

export default {
    data() {
        return {
            token: ""
        }
    },
    created() {
        const localStorageToken = getToken()
        if (!localStorageToken) {
            // console.log('redirecting to home') //eslint-disable-line
            router.push({ name: "home" })
        } else {
            this.token = localStorageToken
        }
    }
}