## 14/03/2020
### Added
- GET /api/user/attendedEvents (returns a list of events in descending order by data, i.e. most recent event goes first. Takes in a token and an optional socID in its query stirng)
- GET /api/soc/getPastEvents (essentially the same as attendedEvents, only this time, it only takes in a socID in its query string, and then returns a list of events that's before the current date which was organised by this soc)

### Changed 
- POST /api/soc/makeAdmin (now accepts a level 1 authorisation token instead of a superadmin token, changed possible error codes)
- check_authorization() no longer tries to load request.args into the AuthSchema and attempt validation