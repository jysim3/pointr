from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from util.auth_services import *
from schemata.event_schemata import *
from util.events import *
from util.participation import *
from util.utilFunctions import *
from util.sanitisation_services import sanitize

api = Namespace('soc', description='Society Attendance Services')

# For getting information on a set of recurrent events
# Usage:
# GET /api/stat/recurEvent?eventID=?
# Returns:
# {["eventID": "ASDA", "name": "AA meeting", "date": "2020-04-03", "attendance": 41], [...]}
@api.route('/recurEvent')
class RecurEvent(Resource):
    def get(self):
        eventID = request.args.get('eventID')
        if (eventID == None):
            return dumps({"status": "Failed", "msg": "No eventID"})

        print(events.fetchRecur(eventID))
        return dumps(events.fetchRecur(eventID))

# Get all the events hosted by a society
@api.route('/eventsHosted')
class EventsHosted(Resource):
    def get(self):
        societyID = request.args.get('societyID')
        if (societyID is None):
            return dumps({"status": "Failed", "msg": "No societyID inputted"})
        eventsList = societies.getEventForSoc(societyID)
        if (eventsList == "No such society"):
            return dumps({"status": "Failed", "msg": "No such society"})
        
        payload = {}
        payload['events'] = []
        payload['societyName'] = eventsList[1]
        for event in eventsList[0]:
            eventJSON = {}
            eventJSON['eventID'] = event[0]
            eventJSON['name'] = event[1]
            eventJSON['society'] = event[3]
            eventJSON['eventDate'] = str(event[2])
            payload['events'].append(eventJSON)
        return dumps(payload)

# TODO: Implement society related flask routings
# Creates a society
# Returns the societyID as part of the result JSON in the "msg" field
@api.route('/create')
class Create(Resource):
    def post():
        data = request.get_json()
        
        result = societies.createSociety(sanitize(data['founder'] if data['founder'] is not None else 'Not Applicable'), sanitize(data['societyName']))
        if (result == "exists already"):
            return dumps({"status": "Failed", "msg": "A society with this name already exists"})
        return dumps({"status": "Success", "msg": result})