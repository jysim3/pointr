from flask import request, jsonify, send_file
from flask_restx import Namespace, Resource, abort, reqparse
from schemata.event_schemata import AttendSchema
from util import events, participation, utilFunctions, auth_services, societies, users, validation_services
from util.sanitisation_services import sanitize
from datetime import datetime
import uuid
from dateutil import tz

api = Namespace('event', description='Event Management Services')

from models.event import *
from models.user import *
from app import db

def generateID(number = None):
    return str(uuid.uuid4().hex).upper()[:5]

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
# TODO: Ask user when they create an event if they want to enable temporary access code
# TODO: Make just ''


@api.route('/accessCode')
class accessCode(Resource):
    def get(self):
        eventID = request.args.get('eventID')
        code = events.getAccessCode(eventID)
        if not code or code == "Event not found": abort(400, "Event not found")

        return jsonify({"accessCode": code})

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

        accessCode = data['accessCode'] if 'accessCode' in data else None

        #time = utilFunctions.getAESTTime()
        time = datetime.now()
        status = participation.register(zID, sanitize(data['eventID']), time, accessCode)
        if (status != "success"):
            abort(403, status)
        payload['status'] = "success"

        return jsonify(payload)
        
    @auth_services.check_authorization(level=2, allowSelf=True, allowSocStaff=True)
    @validation_services.validate_args_with(AttendSchema)
    @api.doc(description="If no zID given in query then will default to attending the token's owner. If zID given in query then will only let that person attend if token owner is that zID or if that zID is an admin of the society")
    def delete(self, token_data, args_data):
        payload = {}
        if ('zID' in args_data):
            payload['status'] = participation.deleteUserAttendance(args_data['zID'], args_data['eventID'])
        else:
            payload['status'] = participation.deleteUserAttendance(token_data['zID'], args_data['eventID'])
        return jsonify(payload)

@api.route('/signAttendanceAdmin')
class adminAttendance(Resource):
    # Takes:
    # Requires an society admin token to work
    # {"eventID": "MEMES", "zID": "z5959595"}
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        data = request.get_json()
        payload = {}

        zID = token_data['zID']
        societyID = societies.getSocIDFromEventID(data['eventID'])
        if (societyID == None):
            abort(403, "Malformed Request, most likely event doesn't exist")
        if societies.checkAdmin(societyID, zID) == False:
            abort(403, "Not signed in as admin")

        # Check whether or not an account exists"
        result = users.checkUser(data['zID'])
        if (result == False):
            abort(403, "This account has not been created")

        results = societies.joinSoc(data['zID'], societyID)
        if (results == "failed"):
            abort(400, "Database problem, joinSoc not successful")

        status = participation.register(data['zID'], data['eventID'], datetime.now())
        if (status != "success"):
            abort(403, "Attendance registration currently not possible for this event")
        payload['status'] = "success"
        return jsonify(payload)


# Accepts /api/event/getAttendance?eventID=SOMETHING
# Returns the CSV file of the attendance info
@api.route('/getAttendance')
class getAttendance(Resource):
    @api.response(400, "Cannot find file")
    @api.response(400, "Malformed Response")
    @auth_services.check_authorization(level=0)
    def get(self, token_data):
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

# This returns all the past events (for all socs the person is participating for)

# This returns all the events (including all of their event infomation)
# NOTE: DEFUNCT ROUTE (WILL NOT BE MAINTAINED FURTHER)
@api.route('/getAllEvents')
class getAllEvents(Resource):
    def get(self):
        result = events.getAllEvents()
        if (result == None):
            abort(400, "Something went wrong, no events found")
        return jsonify(result)

# This deletes a event (removing all the attendance info with it)
@api.route('/deleteEvent')
class deleteEvent(Resource):
    @auth_services.check_authorization(level=1)
    def delete(self, token_data):
        eventID = request.get_json()['eventID']
        socID = societies.getSocIDFromEventID(eventID)
        results = societies.checkAdmin(socID, token_data['zID'])
        if (results == False): abort (403, "Not an admin of the society that's hosting this event")
        results = events.deleteEvent(eventID)
        if (results != "success"):
            abort (400, results)
        return jsonify({"msg": results})

# This closes the input eventID for further attendance marking
@api.route('/closeEvent')
class closeEvent(Resource):
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        eventID = request.get_json()['eventID']

        socID = societies.getSocIDFromEventID(eventID)
        if (societies.checkAdmin(socID, token_data['zID']) == False):
            abort(403, "This user is not an admin of the society which is hosting this event")

        results = events.closeEvent(eventID)
        if (results != "success"):
            abort(400, results)
        return jsonify({"msg": results})

@api.route('/openEvent')
class openEvent(Resource):
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        eventID = request.get_json()['eventID']

        socID = societies.getSocIDFromEventID(eventID)
        if (societies.checkAdmin(socID, token_data['zID']) == False):
            abort(403, "This user is not an admin of the society which is hosting this event")

        results = events.openEvent(eventID)
        if (results != "success"):
            abort(400, results)
        return jsonify({"msg": results})

@api.route("/upcomingEvents")
class upcoming(Resource):
    #@auth_services.check_authorization(level=1)
    def get(self):
        limit = 10 if request.args.get('limit') == None else request.args.get('limit')
        upcoming = events.getAllUpcomingEvents(limit)

        return jsonify(upcoming)

'''
@api.route('/reopenEvent')
class reopenEvent(Resource):
    @areopenEventces.check_authorization(level=1)
    def post(self, token_data):
        eventID = request.get_json()['eventID']

        socID = societies.getSocIDFromEventID()
        if (societies.checkAdmin(socID, token_data['zID']) == False):
            abort(403, "This user is not an admin of the society which is hosting this event")

        results = events.reopenEvent(eventID)
        if (results != "success"):
            abort(400, results)
        return jsonify({"msg": results})
'''


@api.route("/dummy")
class dummy(Resource):
    def post(self):
        from datetime import datetime
        testComposite = CompositeEvent(id="123", name="mem", start=datetime.utcnow(),
        end=datetime.utcnow(), status="open")

        db.session.add(testComposite)
        db.session.commit()

        testBase0 = Event(id="000", name="mem", start=datetime.utcnow(),
        end=datetime.utcnow(), status="open", hasQR=False, hasAccessCode=False,
        hasAdminSignin=False, compositeID="123")

        testBase1 = Event(id="001", name="mem", start=datetime.utcnow(),
        end=datetime.utcnow(), status="open", hasQR=False, hasAccessCode=False,
        hasAdminSignin=False, compositeID="123")
        db.session.add(testBase0)
        db.session.add(testBase1)
        db.session.commit()

        newUser = Users(zID="z5161616", firstname="Steven", lastname="Shen",
        password="12345678", isarc=True, commencementyear=2000, studenttype="undergraduate",
        degreetype="bachelors", superadmin=False, activated=True)
        db.session.add(newUser)
        db.session.commit()

    @api.param
    def get(self):
        event = CompositeEvent.query.filter_by(id="123").first()
        for i in event.getEvents():
            print(i)

@api.route("/dummy2")
class dummy2(Resource):
    def post(self):
        event = Event.query.filter_by(id="000").first()
        user = Users.query.filter_by(zID="z5161616").first()
        event.addAttendance(user)

    def get(self):
        return -1