from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from util.users import *
from util.sanitisation_services import sanitize
from marshmallow import Schema, fields, ValidationError, validates, validate
from util.auth_services import *

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
        return dumps(attendance)
            
    # For creating a user
    # Usage: 
    # POST /api/user
    # Takes: 
    # {zID: "z1234567", name: "Harrison Steyn", token: "fdsmksfksefoi3m.sadsad3r.fda"}
    # Returns: 
    # {"status": "success"}
    def post(self):
        data = request.get_json()
        if ('token' in data):
            token = data['token']
            authorized = authorize_token(token)
            if (authorized['valid']):
                returnVal = createUser(sanitize(data['zID'].lower()), sanitize(data['name']))
                payload = {}
                payload['status'] = returnVal
                return dumps(payload)
            else:
                return dumps(authorized)
        abort(400, 'Malformed Request')