import { getToken } from "@/util.js";

export default {
    data() {
        return {
            token: ""
        }
    },
    created() {
        // TODO: also need to check that token is actually valid.
        this.token = getToken()
    }
}