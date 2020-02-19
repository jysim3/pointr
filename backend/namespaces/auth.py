from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, reqparse
from util import auth_services, users
from util.auth_services import ADMIN, USER
from schemata.auth_schemata import RegisterDetailsSchema, LoginDetailsSchema, TokenSchema
from marshmallow import Schema, fields, ValidationError, validates, validate
from emailPointr import sendActivationEmail
import pprint
import uuid

api = Namespace('auth', description='Authentication & Authorization Services')
    
@api.route('/')

@api.route('/register')
class Register(Resource):
    # @api.response(200, 'Success', token_details)
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @api.response(409, 'Username Taken')
    # @api.expect(auth_details)
    def post(self):
        
        # Ensure the request is json
        if not request.json:
            abort(400, 'Malformed Request')
            
        # Validate the data
        try:
            data = RegisterDetailsSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
            
        # Attempt to create a new user with the username and password
        if not auth_services.register_user(data['zID'], data['password']):
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
class activate(Resource):
    def post(self):
        
        # Check request is json
        if not request.json:
            abort(400, 'Malformed Request')
        
        # Validate data
        try:
            data = TokenSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
        
        # Authorize token and return true or false
        ret_data = auth_services.authorize_token(data['token'], 0)
        if (not ret_data['valid']):
            abort(403, 'Invalid Credentials')
        
        # TODO: Do some validation-related shit
        pprint.pprint(ret_data)
        token_data = ret_data['data']

        result = users.activateAccount(token_data['zID'])
        if (result != 'success'):
            abort(400, result)
        return jsonify({"status": "success"})

@api.route('/login')
class Login(Resource):
    
    # @api.response(200, 'Success', token_details)
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    def post(self):
        # Check request is json
        if not request.json:
            abort(400, 'Malformed Request')
        
        # Validate data
        try:
            data = LoginDetailsSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
        
        # Login and if successful return the token otherwise invalid credentials
        token = auth_services.login(data['zID'], data['password'])
        if (token):
            return jsonify({"token": token})
        else:
            abort(403, 'Invalid Credentials')
        
@api.route('/admin')
class TestAdmin(Resource):
    
    # @api.response(200, 'Success', token_check)
    @api.response(400, 'Malformed Request')
    # @api.expect(token_details)
    def post(self):
        # Check request is json
        if not request.json:
            abort(400, 'Malformed Request')
        
        # Validate data
        try:
            data = TokenSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
        
        # Authorize token and return true or false
        token_data = auth_services.authorize_token(data['token'], ADMIN)
        if (token_data['valid']):
            return jsonify({"valid": True})
        else:
            return jsonify({"valid": False})
            
@api.route('/user')
class TestUser(Resource):
    
    # @api.response(200, 'Success', token_check)
    @api.response(400, 'Malformed Request')
    # @api.expect(token_details)
    def post(self):
        # Check request is json
        if not request.json:
            abort(400, 'Malformed Request')
        
        # Validate data
        try:
            data = TokenSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
        
        # Authorize token and return true or false
        token_data = auth_services.authorize_token(data['token'], USER)
        if (token_data['valid']):
            return jsonify({"valid": True})
        else:
            return jsonify({"valid": False})

@api.route('/validate')
class Authorize(Resource):
    
    # @api.response(200, 'Success', token_check)
    @api.response(400, 'Malformed Request')
    # @api.expect(token_details)
    def post(self):
        # Check request is json
        if not request.json:
            abort(400, 'Malformed Request')
        
        # Validate data
        try:
            data = TokenSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
        
        # Authorize token and return true or false
        token_data = auth_services.authorize_token(data['token'], 0)
        if (token_data['valid']):
            return jsonify({"valid": True})
        else:
            abort(403, 'Invalid Credentials')