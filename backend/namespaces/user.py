from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from util.users import *
from models.models import *
from util.sanitisation_services import sanitize
from marshmallow import Schema, fields, ValidationError, validates, validate

api = Namespace('user', description='User Services')

@api.route('/')
class User(Resource):
    # Returns a list of events this person has attended
    # Usage:
    # GET /api/user?zID=z5214808
    # Returns:
    # [{"eventID": "1239", "name": "Test Event 0", "society": "UNSW Hall", "eventDate": "2019-11-19"}, {"eventID": "1240", "name": "Coffee Night", "society": "UNSW Hall", "eventDate": "2019-11-20"}]
    def get(self):
        zID = request.args.get('zID')
        attendance = getUserAttendance(sanitize(zID.lower()))
        if attendance == 'invalid user': 
            return dumps({"status": "failed"})
        payload = {}
        payload['events'] = []
        payload['zID'] = zID.lower()
        payload['name'] = attendance[1][0]
        for event in attendance[0]:
            eventJSON = {}
            eventJSON['eventID'] = event[1]
            eventJSON['name'] = event[2]
            eventJSON['society'] = event[4]
            eventJSON['eventDate'] = event[3]
            eventJSON['points'] = event[0]
            payload['events'].append(eventJSON)
        return dumps(payload)
        
    # For creating a user
    # Usage: 
    # POST /api/user
    # Takes: 
    # {zID: "z1234567", name: "Harrison Steyn"}
    # Returns: 
    # {"status": "success"}
    def post(self):
        data = request.get_json()
        returnVal = users.createUser(sanitize(data['zID'].lower()), sanitize(data['name']))
        payload = {}
        payload['status'] = returnVal
        return dumps(payload)