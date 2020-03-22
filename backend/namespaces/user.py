from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, reqparse
from util.sanitisation_services import sanitize
from marshmallow import Schema, fields, ValidationError, validates, validate
from util import auth_services, users, participation, validation_services, validation_services
from schemata.auth_schemata import TokenSchema, AuthSchema
from schemata.user_schemata import ZIDSchema, PostPointsSchema
from util.auth_services import ADMIN, USER

api = Namespace('user', description='User Services')
# /user fails but /use doesnt and /user/ doesnt
@api.route('/getUpcomingEvents')
class upcomingEvents(Resource):
    @auth_services.check_authorization(level=0)
    def get(self, token_data):
        zID = token_data['zID']
        results = participation.getUpcomingEvents(zID)
        if (isinstance(results, str) == True):
            abort(400, "Malformed Request")
        return jsonify(results)

# FIXME: Note that the JSON returned from this was changed
@api.route('/getAllSocieties')
class userSocieties(Resource):
    def get(self):
        zID = request.args.get('zID')
        results = participation.getUserSocieties(zID)
        if (isinstance(results, str) == True):
            abort(400, "Malformed Request")
        return jsonify({"status": "success", "message": results})

# NOTE: OUTPUT CHANGED
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
    @auth_services.check_authorization(level=2, allowSelf=True)
    @validation_services.validate_args_with(ZIDSchema)
    def get(self, token_data, args_data):
        attendance = users.getUserAttendance(args_data['zID'].lower())
        return jsonify(attendance)

# NOTE: OUTPUT VALUE CHANGED
@api.route('/info')
@api.param('token', description='Users Token', type='String', required='True')
class info(Resource):
    
    @auth_services.check_authorization(activationRequired=False, level=0)
    def post(self, token_data):

        zID = token_data['zID']
        results = users.getUserInfo(zID)

        if (results == 'failed'):
            abort(400, 'Something went wrong')
        results['zID'] = token_data['zID']
        return jsonify(results)

@api.route('/points')
class Points(Resource):
    
    # Delete user attendance
    # Usage: 
    # DELETE /api/points
    # Takes:
    # {zID: "z5214808", eventID: "13287"}
    # Returns: 
    # {"status": "success"}
    #@auth_services.check_authorization(level=2, allowSelf=True, allowSocStaff=True)
    #@validate_args_with()
    #def delete(self, token_data):
    #    payload = {}
    #    payload['status'] = participation.deleteUserAttendance(sanitize(data['zID'].lower()), sanitize(data['eventID']))
    #    return jsonify(payload)
        
    # Update user attendance
    # Usage: 
    # POST /api/points
    # Takes: 
    # {zID: "z5214808", eventID: "13287", points: "10"}
    # Returns: 
    # {"status": "success"}  "points": 1000
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    @validation_services.validate_with(PostPointsSchema)
    def post(self, data):
        payload = {}
        payload['status'] = participation.changePoints(data['zID'], data['eventID'], data['points'])
        return jsonify(payload)
    
@api.route('/involvedSocs')
class involvedSocs(Resource):
    @auth_services.check_authorization(level=1)
    def get(self, token_data):
        zID = token_data['zID']
        results = users.getInvolvedSocs(zID)
        return jsonify(results)

@api.route('/checkzID')
class checkzID(Resource):
    def get(self):
        zID = request.args.get('zID')
        result = users.checkUser(zID)
        return jsonify({"msg": result})

@api.route('/attendedEvents')
class attended(Resource):
    @auth_services.check_authorization(level=1)
    def get(self, token_data):
        zID = token_data['zID']
        socID = request.args.get('socID')
        results = participation.getUserParticipation(zID, socID)
        return jsonify(results)