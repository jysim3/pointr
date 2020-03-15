## 14/03/2020
### Added

api | file | details
--- | ---- | ---
GET `/api/user/attendedEvents` | namespaces/user.py | returns a list of events in descending order by data, i.e. most recent event goes first. Takes in a token and an optional socID in its query stirng)
GET `/api/soc/getPastEvents` | namespaces/soc.py | essentially the same as attendedEvents, only this time, it only takes in a socID in its query string, and then returns a list of events that's before the current date which was organised by this soc)

### Changed 
api | file | details
--- | ---- | ---
POST `/api/soc/makeAdmin` | namespaces/soc.py | now accepts a level 1 authorisation token instead of a superadmin token, changed possible error codes)
`check_authorization()` | util/validation_services.py | no longer tries to load request.args into the AuthSchema and attempt validation

## 15/03/2020
### Changed

api | file | details
--- | ---- | ---
GET `/api/soc` | namespaces/soc.py | Changed output JSON format to match the rest of the events API output format (i.e. eventID, name, eventDate, location, societyID, societyName)

### In-Progress

api | file | details
--- | ---- | ---
    | APIDOC.md   | Started work on an API documentation file