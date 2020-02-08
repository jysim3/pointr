from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from util.auth_services import *
from models.models import *
from marshmallow import Schema, fields, ValidationError, validates, validate

api = Namespace('auth', description='Authentication & Authorization Services')

class LoginDetailsSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    
class TokenSchema(Schema):
    token = fields.Str(required=True)

@api.route('/register')
class Register(Resource):
    # @api.response(200, 'Success', token_details)
    @api.response(200, 'Success', token_details)
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @api.response(409, 'Username Taken')
    @api.expect(auth_details)
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
        if not register_user(data['username'], data['password']):
            abort(409, 'Username Taken')
            
        # Login the user and return 
        token = login(data['username'], data['password'])
        if (token):
            return dumps({"token": token})
        else:
            abort(403, 'Invalid Username/Password')

@api.route('/login')
class Login(Resource):
    
    @api.response(200, 'Success', token_details)
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @api.expect(auth_details)
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
        token = login(data['username'], data['password'])
        if (token):
            return dumps({"token": token})
        else:
            abort(403, 'Invalid Credentials')
        
@api.route('/test')
class Test(Resource):
    
    @api.response(200, 'Success', token_check)
    @api.response(400, 'Malformed Request')
    @api.expect(token_details)
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
        token_data = authorize_token(data['token'])
        if (token_data.valid):
            return dumps({"valid": True})
        else:
            return dumps({"valid": False})
    