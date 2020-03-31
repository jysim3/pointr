import axios from "axios";
import store from "@/store/index";

let apiURL;
apiURL = 'https://pointr.live';
if (process.env.NODE_ENV === 'development'){
    apiURL = 'http://localhost:5000';
}

export async function fetchAPI(url, method, data) {
    const headers = {}
    const authToken = store.state.user.authToken
    if (authToken) {
        headers.Authorization = authToken;
    }
    if (data) {
        headers['Content-Type'] = 'application/json'
    }

    const options = {
        url: apiURL + url,
        method: method,
        data: data,
        headers: headers
    }

    const response = await axios(options)

    // console.log(options) //eslint-disable-line
    // console.log(response) //eslint-disable-line
    // console.log(response.data) //eslint-disable-line
    // console.log(response.status) //eslint-disable-line

    return response
}

export { apiURL };
