from marshmallow import Schema, fields, ValidationError, validates, validate
from schemata.common_schemata import zidRequired, token, name
    
class ZIDSchema(Schema):
    zID = zidRequired