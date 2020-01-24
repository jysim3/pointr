from flask import request
from flask_restplus import Namespace, Resource, abort, reqparse, fields
from json import dumps
import jwt
from datetime import datetime, date, time, timedelta
from marshmallow import Schema, fields, ValidationError, validates, validate

api = Namespace('auth', description='Authentication & Authorization Services')

# Expiration time on tokens - 60 minutes
token_exp = 60*60
users = {}

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
    @api.expect(login_details)
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
        '''
        global token_exp
        # TODO ensure user is valid
        data = request.get_json()
        token = jwt.encode(
            {
                'exp': datetime.utcnow() + timedelta(seconds=token_exp),
                'iat': datetime.utcnow(),
                'username': data['username']
            }, 
            'secret', algorithm='HS256' # TODO ensure secret is secret
        ) 
        '''
        
@api.route('/test')
class Test(Resource):

    def post(self):
        data = request.get_json()
        token_data = authorize_token(data['token'])
        print(token_data)
        return dumps({"some": "data"})
    
def authorize_token(token):
    try:
        token_data = jwt.decode(
            token,
            'secret',
            algorithms='HS256'
        )
        return {"valid": True, "data": token_data}
    except jwt.InvalidSignatureError:
        print("Received invalid token signature")
        return {"valid": False, "reason": "Invalid token signature"}
    except jwt.ExpiredSignatureError:
        print("Received expired token")
        return {"valid": False, "reason": "Expired token"}
 
def register_user(username, password):
    global users
    if (not users.get(username)):
        users[username] = password
        return True
    return False
        
def login(username, password):
    global users
    if (users.get(username) == password):
        global token_exp
        token = jwt.encode(
            {
                'exp': datetime.utcnow() + timedelta(seconds=token_exp),
                'iat': datetime.utcnow(),
                'username': username
            }, 
            'secret', algorithm='HS256' # TODO ensure secret is secret
        ) 
        return token.decode("utf-8")
    return False
    