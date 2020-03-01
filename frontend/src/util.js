import axios from "axios";

const apiURL = 'http://localhost:5000';

export async function fetchAPI(url, method, data) {
    const headers = {}
    const authToken = getToken()
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

    console.log(options) //eslint-disable-line
    console.log(response) //eslint-disable-line
    console.log(response.data) //eslint-disable-line
    console.log(response.status) //eslint-disable-line

    return response
}

export function getToken() {
    return localStorage.getItem('token')
}

export function setToken(token) {
    return localStorage.setItem('token', token)
}

export function removeToken() {
    return localStorage.removeItem('token')
}

export function isAuthenticated() {
    const localStorageToken = getToken()
    // const tokenIsValid = false
    // TODO: will need to check if user is authenticated (checking token validity on backend) as well as
    // their authorization level (another check on the backend). Best to use Promise.all ?

    if (!localStorageToken) {
        return false
    }

    // TODO: only authorized when permission is not 0
    // TODO: need to check on backend if token is valid as well.

    // return tokenIsValid
    return true // TODO: for debugging purposes user is always authenticated.
}

export function isAdmin() {
    return false
}

export { apiURL };
