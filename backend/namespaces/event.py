from flask import request, jsonify, send_file
from flask_restx import Namespace, Resource, abort, reqparse
from schemata import event_schemata
from util import events, participation, utilFunctions, auth_services
from util.sanitisation_services import sanitize
from datetime import datetime
import uuid

api = Namespace('event', description='Event Management Services')

def generateID(number = None):
    return str(uuid.uuid4().hex)[:10]

# For creating a recurrent event
# Usage: 
# POST /api/event
# Takes:
# { zID: "z5214808", name: "Coffee Night", location: "UNSW Hall", eventDate: "2020-01-01", endDate: "2020-04-04", recurType: "day", recurInterval: 6, "socID": "1DASD", "isRecur": "True"}
# NOTE: isRecur needs to be 1 for this to be a recurrentEvent creation, 0 for single instance event
# NOTE: For single instance events, everything after startDate is not required
# Date is in YYYY-MM-DD
'''
    # Currently, accept four different recurrent parametres, startDate and endDate to indicate how muuch this recurrence will be
    # recurType indicates what kind of recurrence this is (accepts: "day", "week", "month")
    # recurInterval indicates how many of said recurType is inbetween each interval (accepts any int less than 365)
    # Example: startDate = 2020-01-30, endDate = 2020-05-30, recurType = "day", recurInterval = 14 
    # Example Cont.: The above indicates this event occurs every fortnightly starting with 30/1/2020 to 30/5/2020
'''
# Returns:
# { status: "success", "msg": [{"date": 2020-04-04, "eventID": "1FAEA00001"}, {...}}
# or
# { status: "ERROR MESSAGE"}
@api.route('/')
class Event(Resource):

    @api.response(200, 'Success')
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    def post(self):
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

        location = sanitize(str(data['location'])).lower() if 'location' in data else None
        startDate = sanitize(str(data['eventDate'])).lower()
        endDate = sanitize(str(data['endDate']).lower()) if 'endDate' in data else None
        recurType = sanitize(str(data['recurType']).lower()) if 'recurType' in data else None
        recurInterval = sanitize(data['recurInterval']).lower() if 'recurInterval' in data else None
        zID = sanitize(str(data['zID']))
        eventName = sanitize(str(data['name']))
        hasQR = str(data['hasQR'])
        societyID = str(data['socID']) if 'socID' in data else None
        isRecur = str(data['isRecur']) if 'isRecur' in data and data['isRecur'] == 1 else False

        results = None
        if isRecur is not False:
            results = events.createRecurrentEvent(zID, eventID, eventName, startDate, endDate, recurInterval, recurType, hasQR, location, societyID)
        else:
            results = events.createSingleEvent(zID, eventID, eventName, startDate, hasQR, location, societyID)

        if (isinstance(results, tuple) == False):
            return jsonify({"status": "failed", "msg": results})
        return jsonify({"status": "Success", "msg": results[0]})

    # For getting info on an event, i.e. participation information
    # Usage:
    # GET /api/event?eventID=ID
    # Returns: 
    # {"eventID": "1239", "name": "Test Event 0", "participants": [{"zID": "z5161616", "name": "Steven Shen", "points": 1}, {"zID": "z5161798", "name": "Casey Neistat", "points": 1}]}
    @api.response(200, 'Success')
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    def get(self):
        eventID = request.args.get('eventID')
        payload = {}
        attendance = participation.getAttendance(sanitize(eventID))
        if attendance == "failed":
            payload['status'] = 'failed'
        else:
            payload['eventID'] = eventID
            payload['name'] = attendance[1][0]
            payload['hasQR'] = attendance[0][0][4]
            payload['participants'] = []
            for person in attendance[0]:
                personJSON = {}
                personJSON['zID'] = person[3].lower()
                personJSON['name'] = person[2]
                personJSON['points'] = person[0]
                payload['participants'].append(personJSON)
            payload['status'] = 'success'
        return jsonify(payload)
        
@api.route('/onthisday')
class OnThisDay(Resource):
    # Will probably be involved in some kind of a "today's events" type of thing
    # GET /api/events/onthisday?date=2020-04-04&socID=1AEF0 (Note: socID optional)
    # Returns:
    # [{"eventID": "1239", "name": "Test Event 0", "society": "UNSW Hall", "eventDate": "2019-11-19"}, {"eventID": "1240", "name": "Coffee Night", "society": "UNSW Hall", "eventDate": "2019-11-20"}]
    def get(self):
        date = request.args.get('date')
        socID = request.args.get('socID')

        if (date is None):
            return jsonify({"status": "Failed", "msg": "No date provided"})

        return jsonify(utilFunctions.onThisDay(date)) if socID == None else jsonify(utilFunctions.onThisDay(date, socID))

@api.route('/attend')
class Attend(Resource):
    # For adding a user to an event
    # Usage:
    # /api/attend?token=2132.23133.21332
    # Takes: 
    # {eventID': "12332", 'time': "2020-04-04 11:55:59 (i.e. YYYY-MM-DD HH:MM:DD)"}
    @api.response(400, "Malformed Request")
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        data = request.get_json()
        payload = {}

        time = None
        if 'time' in data:
            try:
                time = datetime.strptime(str(data['time']), "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(e)
                abort(400, "Malformed Request")
        else:
            time = datetime.now()
        payload['status'] = participation.register(sanitize(token_data['zID'].lower()), sanitize(data['eventID']), time)
        return jsonify(payload)

@api.route('/getAttendance')
class getAttendance(Resource):
    
    @api.response(400, "Cannot find file")
    @api.response(400, "Malformed Response")
    @auth_services.check_authorization(level=2)
    def get(self):
        eventID = request.args.get('eventID')
        try:
            return send_file(participation.getAttendanceCSV(eventID), as_attachment=True)
        except Exception as e:
            #print(str(e))
            abort(400, "Cannot find file")