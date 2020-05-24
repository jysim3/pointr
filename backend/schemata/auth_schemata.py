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
    name = "Registration Details"
    zID = common_schemata.zidRequired
    password = common_schemata.passwordRequired
    firstName = common_schemata.nameRequired
    lastName = common_schemata.nameRequired
    preferredName = common_schemata.nameRequired
    isArc = common_schemata.booleanRequired
    school = common_schemata.schoolRequired
    faculty = common_schemata.facultyRequired
    degree = common_schemata.degreeRequired
    commencementYear = common_schemata.commencementYearRequired
    #studentType = common_schemata.registrationType
    #degreeType = common_schemata.registrationType

    #@post_load
    #def makeUser(self, data, **kwargs):
    #    return Users(zid=data['zID'], firstname=data['firstName'], lastname=data['lastName'],
    #    password=sha256(data['password'].encode('UTF-8')).hexdigest(), isarc=data['isArc'],
    #    commencementyear=data['commencementYear'], studenttype=data['studentType'],
    #    degreetype=data['degreeType'], superadmin=False, activated=False, description=None)

class LoginDetailsSchema(Schema):
    name = "Login Details"
    zID = common_schemata.zidRequired
    password = common_schemata.passwordRequired
    
class ZIDDetailsSchema(Schema):
    name = "zID"
    zID = common_schemata.zidRequired

class PasswordSchema(Schema):
    name = "Password"
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