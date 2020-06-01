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
                if request.args:
                    args_data = AuthSchema().load(request.args)
                if request.get_json():
                    data = AuthSchema().load(request.get_json())
            except ValidationError as err:
                abort(400, err.messages)

            # Combine args and data
            # args data takes precedence
            data.update(args_data)

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

            user = Users.query.filter_by(zID=token_data['zID'])
            if not user:
                abort(403, "Not a valid user")
            elif user.activated == False and activationRequired == True:
                abort(401, "notActivated")
            elif token_data['permission'] < level:
                abort(403, "Not allowed, not enough permission")
            
            # Allow oneself to modify data if specified
            if allowSelf:
                if 'zID' in data and 'zID' == token_data['zID']:
                    return func(token_data=token_data, *args, **kwargs)

            if allowSuperAdmin:
                if token_data['permission'] == 5:
                    return func(token_data=token_data, *args, **kwargs)
            
            if 'socID' in data:
                society = Societies.query.filter_by(id=data['socID']).first()
                if not society: abort(403, "SocietyID doesn't exist")

                if allowSocMember:
                    members = society.getMembersIDs()
                    if token_data['zID'] not in members: abort(403, "You are not a member of this society")
                    return func(token_data=token_data, *args, **kwargs)

                if allowSocAdmin:
                    admins = society.getAdminsIDs()
                    if token_data['zID'] not in admins: abort(403, "You are not an admin of this society")

                    return func(token_data=token_data, *args, **kwargs)

            if 'eventID' in data:
                # We grant access if the token bearer can have control over eventID
                # I.e. if the user is an admin of the soc that's hosting this event
                # WE need this because socID and eventID dont always come
                event = Event.query.filter_by(id=data['eventID']).first()
                if not event: abort(403, "EventID doesn't exist")

                society = event.getHostSoc()
                # FIXME: Error here is caused by the fact a single event
                # could be hosted by multiple societies
                if allowSocMember:
                    # TODO: Fix this double get
                    members = society[0].getMembersIDs()
                    admins = society[0].getAdminsIDs()
                    members.extend(admins)
                    if token_data['zID'] not in members: abort(403, "You are not a member of this society")

                    return func(token_data=token_data, *args, **kwargs)

                if allowSocAdmin:
                    admins = society[0].getAdminsIDs()
                    if token_data['zID'] not in admins: abort(403, "You are not an admin of this society")

                    return func(token_data=token_data, *args, **kwargs)

            return func(token_data=token_data, *args, **kwargs)

        return wrapper
    return decorator
 
# Low   
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODI2MDI1MzgsImlhdCI6MTU4MjU0MjUzOCwieklEIjoiejUyMTQ4MDgiLCJwZXJtaXNzaW9uIjoxfQ.eOIssA0CfC_aKM14qZBe9T-SHXBkwkAKLkG7VJxbBt4

# High