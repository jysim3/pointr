from marshmallow import Schema, fields, ValidationError, validates, validate
from schemata.common_schemata import zid, token, name

class UserCreationSchema(Schema):
    token = token
    name = name
    zID = zid
    
class ZIDSchema(Schema):
    zID = zid