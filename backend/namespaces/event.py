from flask import request, jsonify, send_file
from flask_restx import Namespace, Resource, abort, reqparse
from schemata import event_schemata
from util import events, participation, utilFunctions, auth_services, societies
from util.sanitisation_services import sanitize
from datetime import datetime
import uuid

api = Namespace('event', description='Event Management Services')

def generateID(number = None):
    return str(uuid.uuid4().hex).upper()[:6]

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
# FIXME: HARRISON FUCKED UP, AND HES TRYING TO JUSTIFY HIS MISTAKE
@api.route('/')
class Event(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    def post(self, token_data):
        data = request.get_json()
        eventID = generateID(5).upper()

        # To determine if an event is being created as a recurrent event
        isRecur = str(data['isRecur']) if 'isRecur' in data and data['isRecur'] == 1 else False

        # For both single and recurrent event
        zID = sanitize(str(token_data['zID']))
        location = sanitize(str(data['location'])).lower() if 'location' in data else None
        startDate = sanitize(str(data['eventDate'])).lower()
        eventName = sanitize(str(data['name']))
        hasQR = str(data['hasQR']) if 'hasQR' in data else False
        societyID = str(data['socID']) if 'socID' in data else None # FIXME: Coordinate with the frontend to ensure this field is always passed
        description = str(data['description']) if 'description' in data else None
        startTime = str(data['startTime']) if 'startTime' in data else None
        endTime = str(data['endTime']) if 'endTime' in data else None

        # Only recurrent event does this
        endDate = sanitize(str(data['endDate']).lower()) if 'endDate' in data else None
        recurType = sanitize(str(data['recurType']).lower()) if 'recurType' in data else None
        recurInterval = sanitize(data['recurInterval']).lower() if 'recurInterval' in data else None

        results = None
        if isRecur is not False:
            results = events.createRecurrentEvent(zID, eventID, eventName, startDate, endDate, recurInterval, recurType, hasQR, location, societyID, description, startTime, endTime)
        else:
            results = events.createSingleEvent(zID, eventID, eventName, startDate, hasQR, societyID, location, description, startTime, endTime)

        if (isinstance(results, tuple) == False):
            return jsonify({"status": "failed", "msg": results})
        return jsonify({"status": "Success", "msg": results[0]})

    # For getting info on an event, i.e. participation information
    # Usage:
    # GET /api/event?eventID=ID
    # Returns: 
    # {"eventName": "memes", "eventDate": "2020-04-01", "location": "UNSW Hall", "societyName": "UNSW Hall", "societyID": "MEMESASD", "attendance": ["points": 1, "isArc" = True, "username": "steven shen", "zID": "z5161616", time: "2020-02-25 00:19:05"]}
    @api.response(200, 'Success')
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @auth_services.check_authorization(level=1)
    def get(self, token_data):
        eventID = request.args.get('eventID')
        attendance = participation.getAttendance(sanitize(eventID))
        if attendance == "failed":
            abort(400, "No such event")

        return jsonify(attendance)

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
    @api.response(403, "Attendance registration currently not possible for this event")
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        data = request.get_json()
        payload = {}

        zID = token_data['zID']
        if ('eventID' not in data):
            abort(400, "Malformed Request")
        time = datetime.now()
        status = participation.register(zID, sanitize(data['eventID']), time)
        if (status != "success"):
            abort(403, "Attendance registration currently not possible for this event")
        payload['status'] = "success"

        return jsonify(payload)

@api.route('/signAttendanceAdmin')
class adminAttendance(Resource):
    # Takes:
    # {"eventID": "MEMES", "zID": "z5959595"}
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        data = request.get_json()
        payload = {}

        zID = token_data['zID']
        societyID = societies.getSocIDFromEventID(data['eventID'])
        if (societyID == None):
            abort(403, "Malformed Request")
        if societies.checkAdmin(societyID, zID) == False:
            abort(403, "Not signed in as admin")

        results = societies.joinSoc(data['zID'], societyID)
        if results != "success":
            abort(400, "Something fucked up")

        status = participation.register(data['zID'], data['eventID'], datetime.now())
        print(status)
        if (status != "success"):
            abort(403, "Attendance registration currently not possible for this event")
        payload['status'] = "success"
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
            abort(400, "Cannot find file")

# This returns all the eventID in place right now (that hasnt happened yet)
@api.route('/getAllEventID')
class getAllEventID(Resource):
    def get(self):
        result = events.getAllEventID()
        if (result == None):
            abort(400, "Something went wrong, no events found")
        return jsonify(result)

# This returns all the events (including all of their event infomation)
@api.route('/getAllEvents')
class getAllEvents(Resource):
    def get(self):
        result = events.getAllEvents()
        if (result == None):
            abort(400, "Something went wrong, no events found")
        return jsonify(result)