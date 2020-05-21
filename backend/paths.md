# Paths to keep

## event

### Event Creation/Deletion/Updating
Status | Method | Route/Query | Description
-------|--------|-------------|------------
Keep | POST  | `/api/event/`| Create an event with given payload
Keep | GET   | `/api/event?eventid={eventid}`| Get an event with given eventid TODO names?
Make | GET   | `/api/event/preview?eventid={eventid}`| Returns preview data (id, image, description, number of attendees/interesteds, start time, location)
Move | DELETE| `/api/event?eventid={eventid}`| Delete an event with given eventid
Make | PATCH | `/api/event?eventid={eventid}`| Update an event with given eventid and payload
Keep | GET   | `/api/event/accessCode?eventid={eventid}`| Get current access Code TODO Consider is it just in GET /api/event///?
Merge with signAttendanceAdmin | POST  | `/api/event/attend`| Body must contain eventid and optionally (for admins) contains a zid to sign in to this event, otherwise signs in self
Keep | DELETE  | `/api/event/attend`| Body must contain eventid and optionally (for admins) contains a zid to delete attendance, otherwise deletes self
Rename | | | POST `/api/event/closeEvent` to PUT `/api/event/close?eventid={eventid}`
Rename | | | DELETE `/api/event/deleteEvent` to DELETE `/api/event?eventid={eventid}` 
Rename | | | GET `/api/event/getAllEvents` to GET `/api/event/all` Returns JSON of every event TODO Specify number?
Rename | | | GET `/api/event/getAllEvents` to GET `/api/event/all/id` Returns id of every event TODO Specify number?
Rename | | | GET `/api/event/getAttendance` to GET `/api/event/attendance?eventid={eventid}` Returns CSV file
Merge/Create | GET | `/api/event/upcoming?day={days In Future}` | Return preview of events coming up in described day (0 is today, 1 is tomorrow etc). Merge of `/api/event/onthisday` and `/api/event/upcomingEvent` to 
Remove | POST | `/api/event/openEvent` | Yeet it
Remove | POST | `/api/event/signAttendanceAdmin` | Merged with attend
Remove | POST | `/api/event/onthisday` | Merged with upcomingEvents to upcoming
Remove | POST | `/api/event/upcomingEvents` | Merged with onthisday to upcoming 


### Misc
Status | Method | Route/Query | Description
-------|--------|-------------|------------
Keep | POST  | `/api/event`

### Delete