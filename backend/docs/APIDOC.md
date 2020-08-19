# API Documentation

## Auth---[namespaces/auth.py](namespaces/auth.py)

api | type | input-parametres (JSON for POST, args for GET) | Description
--- | --- | --- | ---
`/api/auth/register` | POST | `{"zID": "z5161616", "password": "11111111" (8 digits or above), "firstName": "Steven", "lastName": "Shen", "isArc": True, "commencementYear": 2020, "studentType": "undergraduate", "degreeType": "undergraduate"}` | Register new users, all fields are mandatory (i.e. not null)
`/api/auth/activate` | POST | In request headers, `"Authorization": "tokenInfo"`| Attach the user"s emailed temporary token to validate and activate account
`/api/auth/login` | POST | `{"zID": "z5161616", "password": "11111111"}` | Log the user in (provided the right credentials) and return a regular access token
`/api/auth/forgot` | POST | `{"zID": "z5161616"}` | Sends a temporary token to the user"s registered email with a link to reset their password
`/api/auth/reset` | POST | In request headers, `"Authorization": "tokenInfo"`. In JSON, `{"password": "12345678"}` (Must be 8 digits or longer) | Resets the token owner"s password
`/api/auth/validate` | POST | Headers, `"Authorization": "tokenInfo"` | Validates the token passed in

## Event---[namespaces/event.py](namespaces/event.py)

api | type | input-parametres (JSON for POST, args for GET) | Description
--- | --- | --- | ---
`api/event` | POST | `{"zID": "z5161616", "location": "UNSW Hall", "eventDate": "2020-03-10", "name": "Coffee Night", "hasQR": "True", "socID": "ASDFG", "description": "Something something coffee something" (optional), "startTime": "15:45" (optional), "endTime": "19:00" (optional)}` | Create a new (single occurence) event
`api/event` | POST | `{"zID": "z5161616", "location": "UNSW Hall", "eventDate": "2020-03-10", "name": "Coffee Night", "hasQR": "True", "socID": "ASDFG", "description": "Something something coffee something" (optional), "startTime": "15:45" (optional), "endTime": "19:00" (optional), "endDate": "2020-05-10", "recurType": "day", "recurInterval": "7"}` | Create a set of new (recurrently occurence) events
