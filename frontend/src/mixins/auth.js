import jwt from "jsonwebtoken";
import { getToken, isAuthenticated, isAdmin } from "@/util.js";

export default {
    data() {
        return {
            token: "",
            userIsAuthenticated: false,
            userIsAdmin: false
        }
    },
    created() {
        this.userIsAuthenticated = isAuthenticated()
        this.userIsAdmin = isAdmin()
        this.token = getToken()
    },
    methods: {
        getZID() {
            const tokenDecoded = jwt.decode(this.token);
            return tokenDecoded['zID']
        }
    }
}