import { getToken, isAuthenticated } from "@/util.js";

export default {
    data() {
        return {
            token: "",
            isAuthenticated: false
        }
    },
    created() {
        this.isAuthenticated = isAuthenticated()
        this.token = getToken()
    }
}