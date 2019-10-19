export function fetchAPI(url, method, data) {
    if (localStorage.getItem('token')) {
        return (
            fetch(apiUrl + url, {
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
            fetch(apiUrl + url, {
                method: method, // or 'PUT'
                body: JSON.stringify(data), // data can be `string` or {object}!
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
        )
    }
}