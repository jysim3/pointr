API_URL = 'http://127.0.0.1:5000'

fetch = require('node-fetch')

async function postJSON(path, data, token='') {
    try {
        return fetch(API_URL + "/" + path, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify(data)
        });
    } catch (error) {
        console.log("Error posting: " + error);
    }
}

async function runTests() {
    try {
        response = await postJSON("api/auth/register", {
            "zID": "z5214808",
            "password": 'aaaaaaaa'
        })
        console.log(response)
    } catch (error) {
        console.log(error)
    }
    
}

runTests()