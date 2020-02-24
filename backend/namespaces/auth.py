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
        if not auth_services.register_user(data['zID'], data['password'], data['name'] if 'name' in data else "FIXME"):
            abort(409, 'Username Taken')
        
        token = auth_services.generateActivationToken(data['zID'])
        
        # At this point, the user is created, we now send the activation email
        # FIXME: Change this to pointr.live when in production
        sendActivationEmail(f"127.0.0.1:5000/api/auth/activation?token={token}", f"{data['zID']}@student.unsw.edu.au")
        
        return jsonify({"status": "success"})

# NOTE: FIXME: TODO: FOR TESTING ONLY, DO NOT USE IN PRODUCTION

@api.route('/sendActivationEmail')
class activationEmail(Resource):
    def post(self):
        data = request.get_json()
        activationLink = str(uuid.uuid4().hex).upper()
        sendActivationEmail(f"127.0.0.1/api/user/activation?zID={data['username']}&activation={activationLink}", f"{data['username']}@student.unsw.edu.au")

@api.route('/activate')
@api.param('token', description='Users Token', type='String', required='True')
class Activate(Resource):
    
    @auth_services.check_authorization(activationRequired=False, level=0)
    def post(self, token_data):

        result = users.activateAccount(token_data['zID'])
        if (result != 'success'):
            abort(400, result)
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
        
# TODO validate activated

@api.route('/validateSocietyAdmin')
@api.param('token', description='User Token', type='String', required='True')
@api.param('societyID', description='Society ID', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(activationRequired=False, level=5, allowSocStaff=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})
        
@api.route('/validateEventAdmin')
@api.param('token', description='User Token', type='String', required='True')
@api.param('eventID', description='Event ID', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(activationRequired=False, level=5, allowSocStaff=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})