from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE
from schemata import common_schemata

class RegisterDetailsSchema(Schema):
    zID = common_schemata.zid
    password = common_schemata.password
    name = common_schemata.name
    isArc = common_schemata.isArc
    commencementYear = common_schemata.commencementYear
    studentType = common_schemata.registrationType
    degreeType = common_schemata.registrationType

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