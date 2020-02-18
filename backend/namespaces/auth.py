from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, reqparse
from util import auth_services
from marshmallow import Schema, fields, ValidationError, validates, validate

api = Namespace('auth', description='Authentication & Authorization Services')
    
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
            data = LoginDetailsSchema().load(request.get_json())
        except ValidationError as err:
            abort(400, err.messages)
            
        # Attempt to create a new user with the username and password
        if not auth_services.register_user(data['username'], data['password']):
            abort(409, 'Username Taken')

        # Login the user and return 
        token = auth_services.login(data['username'], data['password'])
        if (token):
            return jsonify({"token": token})
        else:
            abort(403, 'Invalid Username/Password')

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
        token = auth_services.login(data['username'], data['password'])
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
        token_data = authorize_token(data['token'], ADMIN)
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
        token_data = authorize_token(data['token'], USER)
        if (token_data['valid']):
            return jsonify({"valid": True})
        else:
            return jsonify({"valid": False})


class LoginDetailsSchema(Schema):
    # FIXME: Check if the username follows the pattern of [zZ][0-9](7)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    
class TokenSchema(Schema):
    token = fields.Str(required=True)