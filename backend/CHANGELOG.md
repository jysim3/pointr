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
N/A   | APIDOC.md   | Started work on an API documentation file

## 21/03/2020
### Changed

api | file | details
--- | ---- | ---
POST `/api/event/attend` | namespaces/event.py | No longer allow attendance marking past endTime, or attendance marking before openTime

### In-Progress

api | file | details
--- | ---- | ---
POST `/api/event/closeEvent` | namespaces/event.py | Manually closes the event, will set the event's endTime field to be "now" on server time
POST `/api/event/openEvent` | namespaces/event.py | Manually opens the event, will set the event's startTime field to be "now" on server time

## 22/03/2020
### Added

api | file | details
--- | ---- | ---
DELETE `/api/event/deleteEvent` | namespaces/event.py | Delete a select event, will also remove any attendance currently associated with the eventID

## 25/03/2020
### Changed

api | file | details
--- | ---- | ---
POST `/api/auth/register` | namespaces/auth.py | Changed the email module we are using to send out emails, now we are abstracting the process away with the Flask-mail module

## 30/03/2020
### Changed

api | file | details
--- | ---- | ---
POST `/api/soc` | namespaces/soc.py | Now accepts images (jpg, png, jpeg) to be uploaded as a part of the society creation process, add the image as a part of the request body to attach image

## 31/03/2020
### Added

api | file | details
--- | ---- | ---
GET `/api/soc/getSocLogo` | namespaces/soc.py | Returns a base64-encoded (but utf-8 decoded to get rid of the b'') string of the image logo of a specified society, None if image wasn't included as a part of the society creation process or error on everything else

### Changed

api | file | details
--- | ---- | ---
GET `/api/events/` | namespaces/event.py | Returns a description field now, as a part of the payload json. Example `{"attendance": [], "description": "", "eventDate": "", "eventName": "", "location": "", "societyID": "", "societyName": ""}`. If description not provided when creating the event, "description" will be a field with value ""

## 01/04/2020
### Added
api | file | details
--- | ---- | ---
POST `/api/auth/changePassword` | namespaces/auth.py | Changes the token bearer's password, 400 on error

## 02/04/2020
### Added
api | file | details
--- | ---- | ---
GET `/api/user/image` | namespaces/user.py | Get the token-bearer's profile photo (if one was set) {"msg": "success", "path": "somepath"}. If photo doesn't exist (or not set), {"msg": "failed", "path": "Image doesn't exist"}
GET `/api/soc/image` | namespaces/soc.py " | Get the socID (in the query string)'s society logo (if one was set) {"msg": "success", "path": "somepath"}. If logo doesn't exist (or not set), {"msg": "failed", "path": "Image doesn't exist"}


### Changed
api | file | details
--- | ---- | ---
GET `/api/user` | namespaces/user.py | Changed the output format to be a user infodump, output format: {"events": [], "firstName": "", "lastName": "", "image": "", "societies": {"member": [], "staff": []}, "zID": ""}
