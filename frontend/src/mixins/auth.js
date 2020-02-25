import jwt from "jsonwebtoken";
import { getToken, isAuthenticated } from "@/util.js";

export default {
    data() {
        return {
            token: "",
            userIsAuthenticated: false
        }
    },
    created() {
        this.userIsAuthenticated = isAuthenticated()
        this.token = getToken()
    },
    methods: {
        getZID() {
            const tokenDecoded = jwt.decode(getToken());
            return tokenDecoded['zID']
        }
    }
}