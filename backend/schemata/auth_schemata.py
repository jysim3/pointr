import jwt, os
from flask_restx import abort
from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE
from schemata import common_schemata
from models.user import Users
from models import User, Event, Society
from marshmallow import post_load
from hashlib import sha256
from pprint import pprint

class PointrSchema(Schema):

    def getDescription(self):
        ret = {}
        fields = vars(self)
        pprint(fields)
        for fieldName in fields['declared_fields']:
            # TODO add more documentation
            field = fields['declared_fields'][fieldName]
            output = {}
            pprint(field)
            output['required'] = field.required
            output['type'] = type(field).__name__
            # output['default'] = field.default | "None"
            # output['description'] = field.description
            ret[fieldName] = output

        return ret

class RegisterDetailsSchema(PointrSchema):
    __schema_name__ = "Registration Details"

    zID = common_schemata.zidRequired
    password = common_schemata.passwordRequired
    firstName = common_schemata.nameRequired
    lastName = common_schemata.nameRequired
    preferredName = common_schemata.name
    discordName = common_schemata.name

    description = fields.Str()
    isArc = common_schemata.booleanRequired

    school = fields.Int(required=False)
    faculty = fields.Int(required=False)
    degree = fields.Int(required=False)
    commencementYear = common_schemata.commencementYear

    @post_load
    def makeUser(self, data, **kwargs):
        data['password'] = sha256(data['password'].encode('utf-8')).hexdigest()
        data['activated'] = False
        data['superadmin'] = False
        return Users(**data)

class LoginDetailsSchema(Schema):
    __schema_name__ = "Login Details"
    zID = common_schemata.zidRequired
    password = common_schemata.passwordRequired

    @post_load
    def getUser(self, data, **kwargs):
        return Users.query.filter_by(zID=data['zID'],
            password=sha256(data['password'].encode('utf-8')).hexdigest()).first()

class ZIDDetailsSchema(Schema):
    __schema_name__ = "zID"
    zID = common_schemata.zidRequired

class PasswordSchema(Schema):
    __schema_name__ = "Password"
    password = common_schemata.passwordRequired
    
class ChangePasswordSchema(Schema):
    __schema_name__ = "Change Password"
    oldPassword = common_schemata.passwordRequired
    newPassword = common_schemata.passwordRequired

class TokenSchema(Schema):
    name = "Token"
    token = common_schemata.tokenRequired

    @post_load
    def getData(self, data, **kwargs):
        jwt_secret = os.environ.get('POINTR_SERVER_SECRET')
        try:
            # Decode token
            token_data = jwt.decode(
                data['token'],
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
        return {**token_data, 'user': request_user}

    
class AuthSchema(Schema):
    eventID = common_schemata.eventID
    societyID = common_schemata.societyID
    zID = common_schemata.zid
    
    @post_load
    def getData(self, data, **kwargs):
        ret = {}
        if 'societyID' in data:
            ret['society'] = Society.findSociety(data['societyID'].hex)
        if 'eventID' in data:
            ret['event'] = Event.getEvent(data['eventID'])
        if 'zID' in data:
            ret['user'] = User.findUser(data['zID'])
        return ret
    class Meta:
        unknown = EXCLUDE
