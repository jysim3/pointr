from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE
from schemata import common_schemata

class ZIDSchema(Schema):
    zID = common_schemata.zidRequired
    
    class Meta:
        unknown = EXCLUDE
    
class EventIDSchema(Schema):
    eventID = common_schemata.eventIDRequired
    
    class Meta:
        unknown = EXCLUDE
    
class SocietyIDSchema(Schema):
    societyID = common_schemata.societyIDRequired
    
    class Meta:
        unknown = EXCLUDE
    
class SocietyIDAndZIDSchema(Schema):
    societyID = common_schemata.societyIDRequired
    zID = common_schemata.zidRequired
    
    class Meta:
        unknown = EXCLUDE