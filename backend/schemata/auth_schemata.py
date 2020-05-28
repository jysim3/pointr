from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE
from schemata import common_schemata
from models.user import Users
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
    preferredName = common_schemata.nameRequired

    description = fields.Str()
    isArc = common_schemata.booleanRequired

    school = fields.Int(required=True)
    faculty = fields.Int(required=True)
    degree = fields.Int(required=True)
    commencementYear = common_schemata.commencementYearRequired

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

class TokenSchema(Schema):
    name = "Token"
    token = common_schemata.tokenRequired
    
class AuthSchema(Schema):
    eventID = common_schemata.eventID
    societyID = common_schemata.societyID
    zID = common_schemata.zid
    
    class Meta:
        unknown = EXCLUDE