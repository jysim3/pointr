from flask import request
from flask_restx import Namespace, Resource, abort, reqparse, fields
from json import dumps
from utils.auth_services import *
import jwt
from datetime import datetime, date, time, timedelta
from marshmallow import Schema, fields, ValidationError, validates, validate

api = Namespace('auth', description='Authentication & Authorization Services')

login_details = api.model('login_details', {
    'username': fields.String(required=True, example='xX_greginator_Xx'),
    'password': fields.String(required=True, example='1234'),
})

class LoginDetailsSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=256))

@api.route('/register')
class Register(Resource):
    # @api.response(200, 'Success', token_details)
    @api.response(400, 'Malformed Request')
    @api.response(409, 'Username Taken')
    #@api.expect(api.model('login_details', {
    #    'username': fields.String(required=True, example='xX_greginator_Xx'),
    #    'password': fields.String(required=True, example='1234'),
    #}))
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
    
    def post(self):
        data = request.get_json()
        token = login(data['username'], data['password'])
        if (token):
            return dumps({"token": token})
        else:
            return dumps({"error": "Failed login"})
        
@api.route('/test')
class Test(Resource):

    def post(self):
        data = request.get_json()
        token_data = authorize_token(data['token'])
        print(token_data)
        return dumps({"some": "data"})
    