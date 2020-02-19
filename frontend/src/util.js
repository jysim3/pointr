const apiURL = 'http://localhost:5000';

export function fetchAPI(url, method, data) {
    if (localStorage.getItem('token')) {
        return (
            fetch(apiURL + url, {
                method: method, // or 'PUT'
                body: JSON.stringify(data), // data can be `string` or {object}!
                headers: {
                    Authorization: 'Token ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
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
                return r
            })
            .then(response => response.json())
            .then(r => {
                console.log(r)//eslint-disable-line
                return r
            })
        )
    }
}

export { apiURL };
