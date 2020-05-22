from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE
from schemata import common_schemata
from models.user import Users
from marshmallow import post_load
from hashlib import sha256

class RegisterDetailsSchema(Schema):
    zID = common_schemata.zid
    password = common_schemata.password
    firstName = common_schemata.name
    lastName = common_schemata.name
    isArc = common_schemata.isArc
    commencementYear = common_schemata.commencementYear
    studentType = common_schemata.registrationType
    degreeType = common_schemata.registrationType

    @post_load
    def makeUser(self, data, **kwargs):
        return Users(zid=data['zID'], firstname=data['firstName'], lastname=data['lastName'],
        password=sha256(data['password'].encode('UTF-8')).hexdigest(), isarc=data['isArc'],
        commencementyear=data['commencementYear'], studenttype=data['studentType'],
        degreetype=data['degreeType'], superadmin=False, activated=False, description=None)

class LoginDetailsSchema(Schema):
    zID = common_schemata.zidRequired
    password = common_schemata.passwordRequired
    
class ZIDDetailsSchema(Schema):
    zID = common_schemata.zidRequired

class PasswordSchema(Schema):
    password = common_schemata.passwordRequired

class TokenSchema(Schema):
    token = common_schemata.tokenRequired
    
class AuthSchema(Schema):
    eventID = common_schemata.eventID
    societyID = common_schemata.societyID
    zID = common_schemata.zid