# Event
Status |To do | Method | Route/Query | Description
-------|-------|--------|-------------|------------
Documented| Keep | POST  | `/api/event/`| Create an event with given payload You must be admin of given society or superadmin
Documented|Keep | GET   | `/api/event?eventid={eventid}`| Get an event with given eventid TODO names?
Documented|Move | DELETE| `/api/event?eventid={eventid}`| Delete an event with given eventid
Documented|Make | PATCH | `/api/event?eventid={eventid}`| Update an event with given eventid and payload
No Work|Make | GET   | `/api/event/preview?eventid={eventid}`| Returns preview data (id, image, description, number of attendees/interesteds, start time, location) NOTE not really needed
No Work|Make | POST  | `/api/event/composite` | Takes in body the message, the composite event (Who the token bearer must be admin of) and the subevent. 
No Work|Make | PUT   | `/api/event/composite/requests?eventid={}&status={1/0}` | Takes in message, the composite event (Who the token bearer must be admin of) and the subevent. 
No Work|Make | GET   | `/api/event/composite/requests?eventid={}` | If admin, return list of requested composite eventing.
No Work|Make | GET | `/api/event/tag?tag={tag}` | Search for events with given tag
No Work|Make | GET | `/api/event/tags` | Returns static list of tags possible
No Work|Keep | GET   | `/api/event/accessCode?eventid={eventid}`| Get current access Code TODO Consider is it just in GET /api/event///?
No Work|Merge with signAttendanceAdmin | POST  | `/api/event/attend`| Body must contain eventid and optionally (for admins) contains a zid to sign in to this event, otherwise signs in self
Documented|Keep | DELETE  | `/api/event/attend`| Body must contain eventid and optionally (for admins) contains a zid to delete attendance, otherwise deletes self
No Work|Rename | | | POST `/api/event/closeEvent` to PUT `/api/event/close?eventid={eventid}`
Documented|Rename | | | DELETE `/api/event/deleteEvent` to DELETE `/api/event?eventid={eventid}` 
No Work|Rename | | | GET `/api/event/getAllEvents` to GET `/api/event/all` Returns JSON of every event TODO Specify number?
No Work|Rename | | | GET `/api/event/getAllEvents` to GET `/api/event/all/id` Returns id of every event TODO Specify number?
No Work|Rename | | | GET `/api/event/getAttendance` to GET `/api/event/attendance?eventid={eventid}` Returns CSV file
Documented|Merge/Create | GET | `/api/event/upcoming?day={days In Future}` | Return preview of events coming up in described day (0 is today, 1 is tomorrow etc). Merge of `/api/event/onthisday` and `/api/event/upcomingEvent` to 
No Work|Remove | POST | `/api/event/openEvent` | Yeet it
No Work|Remove | POST | `/api/event/signAttendanceAdmin` | Merged with attend
No Work|Remove | POST | `/api/event/onthisday` | Merged with upcomingEvents to upcoming
No Work|Remove | POST | `/api/event/upcomingEvents` | Merged with onthisday to upcoming 


# User
status | To do | Method | Route/Query | Description
-------|-------|--------|-------------|------------
No Work|Change | GET  | `/api/user?id={zid}` | Now return description and info on user 
No Work|Add | PATCH | `/api/user` | Optionally takes zid in body, which is info to change.
No Work|Rename and modify | GET | `/api/user/attendedEvents` to `/api/user/events/upcoming` | Returns preview of upcoming events attended and interested in. + Laater on pos and offset
No Work|Rename and modify | GET | `/api/user/attendedEvents` to `/api/user/events/past` | Returns preview of past events attended and interested in. + Laater on pos and offset
No Work|Remove | GET | `/api/checkzID` | Yeet
No Work|Merge | POST | `/api​/user​/description` | with POST `/api/user/`
No Work|Merge | GET | `/api​/user​/description` | with GET `/api/user/`
No Work|Rename | GET | `/api​/user​/involvedSocs` and `/api​/user​/getAllSocieties` | to `/api/user/societies/member` returns preview of all societies (Take pos and offset in future)
No Work|Merge | POST | `/api​/user​/image` | with POST `/api/user/`
No Work|Merge | GET | `/api​/user​/image` | with GET `/api/user/`
No Work|Yeet | POST | `/api​/user​/points`

# Soc
Status | To do | Method | Route/Query | Description
-------|-------|--------|-------------|------------
No Work|Keep | GET | `/api/soc?socid={socid}` | Return full description data of given society
No Work|Keep | POST | `/api/soc?socid={socid}` | Making a new society (must be superadmin)
No Work|Make | PATCH | `/api/soc?socid={socid}` | Update society info (must be admin)
No Work|Make | GET | `/api/soc/tag?tag={tag}` | Search for socs with given tag
No Work|Make | GET | `/api/soc/tags` | Returns static list of tags possible
No Work|Make | PUT | `/api/soc/archive?socid={}&status={1/0}` |  Turn society on/off (must be superadmin)
No Work|Merge | POST | `/api​/soc​/description` | with `/api/soc?socid={socid}`
No Work|Merge | GET | `/api​/soc​/description` | with `/api/soc?socid={socid}`
No Work|Rename and modify | GET | `/api/soc/events` to `/api/soc/events/upcoming` | Returns preview of upcoming events attended and interested in. + Laater on pos and offset
No Work|Rename and modify | GET | `/api/soc/getPastEvents` to `/api/soc/events/past` | Returns preview of past events attended and interested in. + Later on pos and offset
No Work|Rename | GET | `/api​/soc​/getAllSocs` | to `/api​/soc​/all`
No Work|Merge | GET | `/api​/soc​/getSocLogo` | with `/api/soc`
No Work|Merge | POST | `/api​/soc​/image` | with `/api/soc`
No Work|Merge | GET | ​`/api​/soc​/image` | with `/api/soc`
No Work|Create | GET | `/api/soc/requests?socid={socid}` | Shows preview data on people requesting to join given society (must be done by soc admin)
No Work|Create | PUT | `/api/soc/requests?socid={socid}&zid={}&status={1/0}` | Removes/adds member to the society (must be done by soc admin)
No Work|Modify | POST | `/api​/soc​/join` | Has 3 modes: If society is invitation only, rejects. If society is application it takes in a message and admin can find this in GET `/api/soc/requests/` and accept in PUT `/api/soc/requests/`.
No Work|Add | PUT | `/api​/soc​/leave` | Removes member from society, can be done by self, admin or superadmin optionally contain zid to not use token bearer.
No Work|Add | PUT | `/api​/soc​/leave/all` | Removes all members from society, must be done by superadmin.
No Work|Remove | POST | `/api​/soc​/makeAdmin` | Done by modifying database directly (use makeAdmin.py)
No Work|Keep | POST | `/api​/soc​/staff`
No Work|Keep | GET | ​`/api​/soc​/staff` | Keep em but call admin instead
No Work|Keep | DELETE | `/api​/soc​/staff`

## TODO Non zid people

# Other
Status |To do | Method | Route/Query | Description
-------|-------|--------|-------------|------------
No Work|Keep | POST | ​`/api​/other​/enquire`
No Work|Remove | GET | `/api​/other​/onThisDay`

# Auth
Status | To do | Method | Route/Query | Description
-------|-------|--------|-------------|------------
Documented|Keep | POST | `/api​/auth​/activate`
Documented|Rename | POST | `/api​/auth​/changePassword` | to `/api​/auth​/change`
Documented|Keep | POST | `/api​/auth​/forgot`
Documented|Keep | POST | `​/api​/auth​/login`
Done|Remove | POST | `/api​/auth​/permission` | Use value in token instead
Documented|Keep | POST | `​/api​/auth​/register`
Documented|Keep | POST | `​/api​/auth​/reset` | Used for 
Done|Keep | POST | `​/api​/auth​/validate`
No Work|Keep (for now) | POST | `​/api​/auth​/validateSelf`
No Work|Keep (for now) | POST | `​/api​/auth​/validateEventAdmin`
No Work|Keep (for now) | POST | `/api​/auth​/validateSocietyAdmin`