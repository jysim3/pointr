import jwt
from datetime import datetime, date, time, timedelta
from util.users import checkUserInfo, checkUser, createUser
from util.societies import getSocIDFromEventID, getAdminsForSoc
from flask_restx import abort
from flask import request
from schemata.auth_schemata import TokenSchema, AuthSchema
from marshmallow import ValidationError
from util.validation_services import validate_args_with
import pprint
import os, sys

# Expiration time on tokens - 60 minutes #FIXME
token_exp = 1000*60
activationTokenTimeout = 1000*60
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
            # return {"valid": False, "reason": "Permission denied"}
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

def register_user(zID, name, password, isArc=True):
    if (checkUser(zID) == False): #TODO fixe isArc
        return True if createUser(zID, name, password, isArc) == "Success" else False
    return False

def login(zID, password):
    results = checkUserInfo(zID, password)
    if (results == True):
        global token_exp
        token = jwt.encode(
            {
                'exp': datetime.utcnow() + timedelta(seconds=token_exp),
                'iat': datetime.utcnow(),
                'zID': zID,
                'permission': 1 # TODO Make it so admins and users can be created
            }, 
            jwt_secret, algorithm='HS256' 
        ) 
        return token.decode("utf-8")
    return None
    
def generateActivationToken(zID):
    global activationTokenTimeout
    token = jwt.encode(
        {
            'exp': datetime.utcnow() + timedelta(seconds=activationTokenTimeout),
            'iat': datetime.utcnow(),
            'zID': zID,
            'permission': 0
        }, 
        jwt_secret, algorithm='HS256' 
    ) 
    return token.decode("utf-8")

def authorizeActivationToken(token):
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
                try:
                    args_data = AuthSchema().load(request.args)
                except ValidationError as err:
                    abort(400, err.messages)

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

                # Check if eventID exists in query
                if (allowSocStaff and 'eventID' in args_data):
                    # if so then get society of event
                    societyID = getSocIDFromEventID(args_data['societyID'])
                    # check this zID is an admin of this society
                    admins = getAdminsForSoc(societyID)
                    if (token_data['zID'] in admins):
                        # if so allow
                        return func(token_data=token_data, *args, **kwargs)

                # if societyID exists in query
                if (allowSocStaff and 'societyID' in args_data):

                    # check if zID is admin of society
                    admins = getAdminsForSoc(args_data['societyID'])
                    
                    pprint.pprint(admins)
                    if (token_data['zID'] in admins):
                        # if so allow
                        return func(token_data=token_data, *args, **kwargs)
                                        
                # Check permissions on token
                if (int(token_data['permission']) >= level):
                    return func(token_data=token_data, *args, **kwargs)
                    # Allow a token of a zID access data pertaining to that zID
                elif (allowSelf and 'zID' in args_data and token_data['zID'] == args_data['zID']):
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