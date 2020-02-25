from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE
from schemata import common_schemata

class RegisterDetailsSchema(Schema):
    zID = common_schemata.zid
    password = common_schemata.password
    
class LoginDetailsSchema(Schema):
    zID = common_schemata.zid
    password = common_schemata.password

class TokenSchema(Schema):
    token = common_schemata.tokenRequired
    
class AuthSchema(Schema):
    eventID = common_schemata.eventID
    societyID = common_schemata.societyID
    zID = common_schemata.zid