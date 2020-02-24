import jwt from "jsonwebtoken";
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
    },
    methods: {
        getZID() {
            const tokenDecoded = jwt.decode(getToken());
            return tokenDecoded['zID']
        }
    }
}