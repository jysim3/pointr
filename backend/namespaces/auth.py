from flask import request, jsonify, request
from flask_restx import Namespace, Resource, abort, reqparse
from util import auth_services, users
from util.auth_services import ADMIN, USER
from schemata.auth_schemata import RegisterDetailsSchema, LoginDetailsSchema, TokenSchema
from marshmallow import Schema, fields, ValidationError, validates, validate
from emailPointr import sendActivationEmail
from util.validation_services import validate_with, validate_args_with
import pprint
import uuid

api = Namespace('auth', description='Authentication & Authorization Services')

@api.route('/register')
class Register(Resource):
    # @api.response(200, 'Success', token_details)
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @api.response(409, 'Username Taken')
    @validate_with(RegisterDetailsSchema)
    def post(self, data):
            
        # Attempt to create a new user with the username and password
        zID = data['zID']
        password = data['password']
        name = data['name'] if 'name' in data else "John Doe"
        isArc = data['isArc'] if 'isArc' in data else True
        commencementYear = data['commencementYear'] if 'commencementYear' in data else None
        studentType = data['studentType'] if 'studentType' in data else "domestic"
        degreeType = data['degreeType'] if 'degreeType' in data else "undergraduate"

        if not auth_services.register_user(zID, name, password, isArc, int(commencementYear), studentType, degreeType):
            abort(409, 'Username Taken')
        
        token = auth_services.generateActivationToken(data['zID'])
        #print(token)

        # At this point, the user is created, we now send the activation email
        # FIXME: Change this to pointr.live (in frontend) when in production
        sendActivationEmail(f"https://pointer.live/activate/{token}", f"{data['zID']}@student.unsw.edu.au")

        return jsonify({"status": "success"})

@api.route('/activate')
@api.param('token', description='Users Token', type='String', required='True')
class Activate(Resource):
    @api.response(400, "Malformed Request")
    @api.response(403, "Already activated")
    @auth_services.check_authorization(activationRequired=False, level=0)
    def post(self, token_data):

        result = users.activateAccount(token_data['zID'])
        if (result == "failed"):
            abort(400, "Malformed Request")
        elif (result == "already activated"):
            abort(403, "Already activated")
        return jsonify({"status": "success"})

@api.route('/login')
class Login(Resource):
    
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @validate_with(LoginDetailsSchema)
    def post(self, data):
        
        # Login and if successful return the token otherwise invalid credentials
        token = auth_services.login(data['zID'], data['password'])
        if (token):
            return jsonify({"token": token})
        else:
            abort(403, 'Invalid Credentials')

@api.route('/permission')
class Login(Resource):
    
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @auth_services.check_authorization(activationRequired=False, level=0)
    def post(self, token_data):
        return jsonify({"permission": token_data['permission']})

@api.route('/validate')
@api.param('token', description='User Token', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(activationRequired=False, level=0)
    def post(self, token_data):
        return jsonify({"valid" : "true"})

# Validation functions
@api.route('/validateSelf')
@api.param('token', description='User Token', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(activationRequired=False, level=5, allowSelf=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})

@api.route('/validateSocietyAdmin')
@api.param('token', description='User Token', type='String', required='True')
@api.param('societyID', description='Society ID', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(level=5, allowSocStaff=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})
        
@api.route('/validateEventAdmin')
@api.param('token', description='User Token', type='String', required='True')
@api.param('eventID', description='Event ID', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(level=5, allowSocStaff=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})