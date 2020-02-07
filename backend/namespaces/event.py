from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from utils.auth_services import *
from models.models import *
from schemata.event_schemata import *

api = Namespace('event', description='Event Management Services')

# For creating an event
# Usage: 
# POST /api/event
# Takes:
# { zID: "z5214808", name: "Coffee Night", eventDate: "2019-11-19"}
# Date is in YYYY-MM-DD
# Returns:
# { status: "success", eventID: "1234F"}
# or
# { status: "ERROR MESSAGE"}

def sanitize(input):
    return re.sub("[^\w ']", "", input)

def generateID(number):
    id = ""
    for x in range(0, number):
        id += random.choice(string.hexdigits)
    return id

@api.route('/')
class Event(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    
    def post(self):
        if not request.json:
            abort(400, 'Malformed Request')
        data = request.get_json()
        eventID = generateID(5).upper()
        if not 'hasQR' in data:
            data['hasQR'] = False
        elif data['hasQR'].lower() == "true":
            data['hasQR'] = True
        elif data['hasQR'].lower() == "false":
            data['hasQR'] = False
        else:
            data['hasQR'] = False
                
        payload = {}
        payload['status'] = utilFunctions.createEvent(sanitize(str(data['zID']).lower()), sanitize(str(eventID)), sanitize(str(data['name'])), sanitize(str(data['eventDate'])), data['hasQR'])
        if payload['status'] == 'success':
            payload['eventID'] = eventID
        return dumps(payload)
    
    @api.response(200, 'Success')
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    def get(self):
        eventID = request.args.get('eventID')
        payload = {}
        attendance = utilFunctions.getAttendance(sanitize(eventID))
        if attendance == "failed":
            payload['status'] = 'failed'
        else:
            payload['eventID'] = eventID
            payload['name'] = attendance[1]
            payload['hasQR'] = False
            payload['participants'] = []
            for person in attendance[0]:
                personJSON = {}
                print(person)
                # Fix Stevens shit formatting
                personJSON['zID'] = person[0][0][0].lower()
                personJSON['name'] = person[0][0][1]
                personJSON['points'] = person[1]
                payload['participants'].append(personJSON)
            payload['status'] = 'success'
        return dumps(payload)

# For getting info on an event
# Usage:
# GET /api/event?eventID=ID
# Returns: 
# {"eventID": "1239", "name": "Test Event 0", "participants": [{"zID": "z5161616", "name": "Steven Shen", "points": 1}, {"zID": "z5161798", "name": "Casey Neistat", "points": 1}]}