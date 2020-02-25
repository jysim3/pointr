const apiURL = 'http://localhost:5000';

export function fetchAPI(url, method, data) {
    if (localStorage.getItem('token')) {
        return (
            fetch(apiURL + url, {
                method: method, // or 'PUT'
                body: JSON.stringify(data), // data can be `string` or {object}!
                headers: {
                    Authorization: getToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(r => {
                console.log(r)//eslint-disable-line
                const j = r.json()
                j.status = r.status
                return j
            })
        )
    } else {

        return (
            fetch(apiURL + url, {
                method: method, // or 'PUT'
                body: JSON.stringify(data), // data can be `string` or {object}!
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(r => {
                console.log(r)//eslint-disable-line
                const j = r.json()
                return j
            })
        )
    }
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

    if (!localStorageToken) {
        return false
    }

    // TODO: only authorized when permission is not 0

    // return tokenIsValid
    return true // TODO: for debugging purposes user is always authenticated.
}

export { apiURL };
