import jwt
from datetime import datetime, date, time, timedelta
from util.users import checkUserInfo, checkUser, createUser, checkActivation
from util.societies import getSocIDFromEventID, getAdminsForSoc
from flask_restx import abort
from flask import request
from schemata.auth_schemata import TokenSchema, AuthSchema
from marshmallow import ValidationError
from util.validation_services import validate_args_with
import pprint
import os, sys

# Expiration time on tokens - 60 minutes 
token_exp = 1000*60
activationTokenTimeout = 1000*60
forgotTokenTimeout = 1000*60
ADMIN = 'Admin'
USER = 'User'

if (os.environ.get('POINTR_SERVER_SECRET') == None):
    print("Missing environment secret key for email address. Set env variable POINT_EMAIL_PASSWORD to the password.")
    sys.exit()
jwt_secret = os.environ.get('POINTR_SERVER_SECRET')

def authorize_token(token, permission):
    try:
        token_data = jwt.decode(
            token,
            jwt_secret,
            algorithms='HS256'
        )
        global ADMIN, USER
        if (permission == token_data['permission']):
            return {"valid": True, "data": token_data}
        elif (token_data['permission'] == ADMIN and permission == USER):
            return {"valid": True, "data": token_data}
        else:
            return {"valid": True, "data": token_data}
    except jwt.InvalidSignatureError:
        print("Received invalid token signature")
        return {"valid": False, "reason": "Invalid token"}
    except jwt.ExpiredSignatureError:
        print("Received expired token")
        return {"valid": False, "reason": "Expired token"}
    except jwt.DecodeError:
        print("Received invalid token data")
        return {"valid": False, "reason": "Invalid token"}
    return {"valid": False, "reason": "Unknown"}

def authorize(token, permission):
    try:
        token_data = jwt.decode(
            token,
            jwt_secret,
            algorithms='HS256'
        )
        global ADMIN, USER
        if (permission == token_data['permission']):
            return {"valid": True, "data": token_data}
        elif (token_data['permission'] == ADMIN and permission == USER):
            return {"valid": True, "data": token_data}
        else:
            abort(401, "Permission Denied")
    except jwt.InvalidSignatureError:
        print("Received invalid token signature")
        abort(403, 'Invalid Credentials')
    except jwt.ExpiredSignatureError:
        print("Received expired token")
        abort(401, 'Expired Token')
    except jwt.DecodeError:
        print("Received invalid token data")
        abort(403, 'Invalid Credentials')
    abort(400, 'Malformed Request')

def login(zID, password):
    results = checkUserInfo(zID, password)
    if (results == False):
        return None
    global token_exp
    token = jwt.encode(
        {
            'exp': datetime.utcnow() + timedelta(seconds=token_exp),
            'iat': datetime.utcnow(),
            'zID': zID,
            'permission': 1 if results == 1 else 5,
            'activation': checkActivation(zID),
            'type': 'normal'
        }, 
        jwt_secret, algorithm='HS256' 
    ) 
    return token.decode("utf-8")
    
def generateActivationToken(zID):
    global activationTokenTimeout
    token = jwt.encode(
        {
            'exp': datetime.utcnow() + timedelta(seconds=activationTokenTimeout),
            'iat': datetime.utcnow(),
            'zID': zID,
            'permission': 0,
            'activation': 0,
            'type': 'activation'
        }, 
        jwt_secret, algorithm='HS256' 
    ) 
    return token.decode("utf-8")

def generateForgotToken(zID):
    global forgotTokenTimeout
    token = jwt.encode(
        {
            'exp': datetime.utcnow() + timedelta(seconds=forgotTokenTimeout),
            'iat': datetime.utcnow(),
            'zID': zID,
            'permission': 0,
            'activation': 0,
            'type': 'forgot'
        }, 
        jwt_secret, algorithm='HS256' 
    ) 
    return token.decode("utf-8")

def authorizeOneTimeToken(token):
    try:
        token_data = jwt.decode(
            token,
            jwt_secret,
            algorithms='HS256'
        )
        return {"valid": True, "token_data": token_data}
    except jwt.InvalidSignatureError:
        print("Received invalid token signature")
        abort(403, 'Invalid Credentials')
    except jwt.ExpiredSignatureError:
        print("Received expired token")
        abort(401, 'Expired Token')
    except jwt.DecodeError:
        print("Received invalid token data")
        abort(403, 'Invalid Credentials')
    abort(400, 'Malformed Request')

def check_authorization(activationRequired=True, level=0, allowSelf=False, allowSocStaff=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Validate token
                args_data = {}
                data = {}
                
                '''
                try:
                    args_data = AuthSchema().load(request.args)
                except ValidationError as err:
                    abort(400, err.messages)
                '''
                
                
                try:
                    token = TokenSchema().load({"token": request.headers.get('Authorization')})
                except ValidationError as err:
                    abort(400, err.messages)

                # Decode token
                token_data = jwt.decode(
                    token['token'],
                    jwt_secret,
                    algorithms='HS256'
                )
                
                data = None
                if request.get_json() != None:
                    data = request.get_json()
                
                if (activationRequired and not token_data['activation']):
                    abort('403', 'Activation Required')

                # Check if eventID exists in query
                if (allowSocStaff and 'eventID' in args_data):
                    # if so then get society of event
                    societyID = getSocIDFromEventID(args_data['eventID'])
                    # check this zID is an admin of this society
                    admins = getAdminsForSoc(societyID)
                    if (token_data['zID'].lower() in admins):
                        # if so allow
                        return func(token_data=token_data, *args, **kwargs)
                elif (allowSocStaff and 'eventID' in data):
                    societyID = getSocIDFromEventID(data['eventID'])
                    admins = getAdminsForSoc(societyID)
                    if (token_data['zID'].lower() in admins):
                        return func(token_data=token_data, *args, **kwargs)


                # if societyID exists in query
                if (allowSocStaff and 'societyID' in args_data):

                    # check if zID is admin of society
                    admins = getAdminsForSoc(args_data['societyID'])
                    
                    pprint.pprint(admins)
                    if (token_data['zID'].lower() in admins):
                        # if so allow
                        return func(token_data=token_data, *args, **kwargs)
                elif (allowSocStaff and 'societyID' in data) or (allowSocStaff and 'socID' in data):
                    admins = getAdminsForSoc(data['societyID']) if 'societyID' in data else getAdminsForSoc(data['socID'])
                    if (token_data['zID'].lower() in admins):
                        return func(token_data=token_data, *args, **kwargs)

                # Check permissions on token
                if (int(token_data['permission']) >= level):
                    return func(token_data=token_data, *args, **kwargs)
                    # Allow a token of a zID access data pertaining to that zID
                elif (allowSelf and 'zID' in args_data and token_data['zID'].lower() == args_data['zID'].lower()):
                    return func(token_data=token_data, *args, **kwargs)
                else:
                    abort(401, "Permission Denied")
            except jwt.InvalidSignatureError:
                print("Received invalid token signature")
                abort(403, 'Invalid Credentials')
            except jwt.ExpiredSignatureError:
                print("Received expired token")
                abort(401, 'Expired Token')
            except jwt.DecodeError:
                print("Received invalid token data")
                abort(403, 'Invalid Credentials')
            abort(400, 'Malformed Request')
        return wrapper
    return decorator
 
# Low   
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODI2MDI1MzgsImlhdCI6MTU4MjU0MjUzOCwieklEIjoiejUyMTQ4MDgiLCJwZXJtaXNzaW9uIjoxfQ.eOIssA0CfC_aKM14qZBe9T-SHXBkwkAKLkG7VJxbBt4

# High