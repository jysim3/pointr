from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from util.users import *
from util.sanitisation_services import sanitize
from marshmallow import Schema, fields, ValidationError, validates, validate
from util.auth_services import *
from schemata.auth_schemata import TokenSchema
from schemata.user_schemata import UserCreationSchema, ZIDSchema

api = Namespace('user', description='User Services')

@api.route('/')
class User(Resource):
    # Returns a list of events this person has attended
    # Usage:
    # GET /api/user
    # Takes:
    # {zID: "z1111111"}
    # Returns:
    # [{"eventID": "1239", "name": "Test Event 0", "society": "UNSW Hall", "eventDate": "2019-11-19"}, {"eventID": "1240", "name": "Coffee Night", "society": "UNSW Hall", "eventDate": "2019-11-20"}]
    @api.response(400, 'Malformed Request')
    # @api.description('Retrieves data on user')
    def get(self):
        if not request.json:
            abort(400, 'Malformed Request')
        # TODO token here
        # Validate data
        try:
            data = ZIDSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
            
        zID = data['zID']
        attendance = getUserAttendance(sanitize(zID.lower()))
        return dumps(attendance)
            
    # For creating a user
    # Usage: 
    # POST /api/user
    # Takes: 
    # {zID: "z1234567", name: "Harrison Steyn", token: "fdsmksfksefoi3m.sadsad3r.fda"}
    # Returns: 
    # {"status": "success"}
    @api.response(400, 'Malformed Request')
    @api.response(401, 'Expired Token')
    @api.response(403, 'Invalid Credentials')
    # @api.description('Creates a user with given details')
    def post(self):
        if not request.json:
            abort(400, 'Malformed Request')
        
        # Validate data
        try:
            data = UserCreationSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
            
        authorized = authorize(data['token'], ADMIN)
        
        if (authorized['valid']):
            returnVal = createUser(sanitize(data['zID'].lower()), sanitize(data['name']))
            payload = {}
            payload['status'] = returnVal
            return dumps(payload)
        else:
            return dumps(authorized)
        abort(400, 'Malformed Request')