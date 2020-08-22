import jwt
from datetime import datetime, date, time, timedelta
from flask_restx import abort
from flask import request
from schemata.auth_schemata import TokenSchema, AuthSchema
from marshmallow import ValidationError
import pprint
import os, sys
from models.society import Societies
from models.event import Event
from models.user import Users

# Expiration time on tokens - 60 minutes 
token_exp = 1000*60
activationTokenTimeout = 1000*60
forgotTokenTimeout = 1000*60

if (os.environ.get('POINTR_SERVER_SECRET') == None):
    print("Missing environment secret key for email address. Set env variable POINT_EMAIL_PASSWORD to the password.")
    sys.exit()
jwt_secret = os.environ.get('POINTR_SERVER_SECRET')

def generateLoginToken(user):
    permission = 5 if user.superadmin == True else 1
    global token_exp
    token = jwt.encode(
        {
            'exp': datetime.utcnow() + timedelta(seconds=token_exp),
            'iat': datetime.utcnow(),
            'zID': user.zID,
            'permission': 0 if user.activated == False else 1 if user.superadmin == False else 5,
            'type': 'normal'
        }, 
        jwt_secret, algorithm='HS256' 
    ) 
    return token.decode("utf-8")
    
def generateActivationToken(user):
    global activationTokenTimeout
    token = jwt.encode(
        {
            'exp': datetime.utcnow() + timedelta(seconds=activationTokenTimeout),
            'iat': datetime.utcnow(),
            'zID': user.zID,
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

def checkAuthorization(activationRequired=True, level=0, allowSelf=False, allowSuperAdmin=False, allowSocAdmin=False, allowSocMember=False):
    def decorator(func):
        def wrapper(*args, **kwargs):

            args_data = {}
            data = {}


            token = TokenSchema().load({"token": request.headers.get('Authorization')})
            try:
                # Combine args and data
                # args data takes precedence
                request_data = {}
                if request.get_json(): 
                    request_data.update(request.get_json())
                if request.args:
                    request_data.update(request.args)
                if request_data:
                    data = AuthSchema().load(request_data)
                user = data['user'] if 'user' in data else None
                event = data['event'] if 'event' in data else None
                society = data['society'] if 'society' in data else None
            except ValidationError as err:
                abort(400, err.messages)


            try:
                # Decode token
                token_data = jwt.decode(
                    token['token'],
                    jwt_secret,
                    algorithms='HS256'
                )
            except jwt.InvalidSignatureError:
                abort(403, 'Invalid Credentials')
            except jwt.ExpiredSignatureError:
                abort(401, 'Expired Token')
            except jwt.DecodeError:
                abort(403, 'Invalid Credentials')

            request_user = Users.query.filter_by(zID=token_data['zID']).first()
            if not request_user:
                abort(403, "Internal error: this user should not exist")
            elif request_user.activated == False and activationRequired == True:
                abort(401, "notActivated")
            elif token_data['permission'] < level:
                abort(403, "Not allowed, not enough permission")
            
            # Allow oneself to modify data if specified
            if allowSelf:
                if user and user.zID == request_user.zID:
                    return func(token_data=token_data, *args, **kwargs)

            if allowSuperAdmin:
                if request_user.superadmin:
                    return func(token_data=token_data, *args, **kwargs)
            
            if allowSocMember or allowSocAdmin:
                if 'eventID' in request_data:
                    # We grant access if the token bearer can have control over eventID
                    # I.e. if the user is an admin of the soc that's hosting this event
                    # WE need this because socID and eventID dont always come
                    if not event: abort(403, "EventID doesn't exist")

                society = society if society else event.getHostSoc()[0]
                if not society: abort(403, "Society doesn't exist")

                if allowSocMember:
                    members = society.getMembersIDs()
                    admins = society[0].getAdminsIDs()
                    members.extend(admins)
                    if request_user.zID not in members: abort(403, "You are not a member of this society")
                    return func(token_data=token_data, *args, **kwargs)

                if allowSocAdmin:
                    admins = society.getAdminsIDs()
                    if request_user.zID not in admins: abort(403, "You are not an admin of this society")

                    return func(token_data=token_data, *args, **kwargs)

            return func(token_data=token_data, *args, **kwargs)

        return wrapper
    return decorator
 
# Low   
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODI2MDI1MzgsImlhdCI6MTU4MjU0MjUzOCwieklEIjoiejUyMTQ4MDgiLCJwZXJtaXNzaW9uIjoxfQ.eOIssA0CfC_aKM14qZBe9T-SHXBkwkAKLkG7VJxbBt4

# High