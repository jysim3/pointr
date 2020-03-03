from marshmallow import Schema, fields, ValidationError, validates, validate
from schemata import common_schemata

class ZIDSchema(Schema):
    zID = common_schemata.zidRequired
    
class DeletePointsSchema(Schema):
    ZID = common_schemata.zid
    eventID = common_schemata.eventIDRequired
    
class PostPointsSchema(Schema):
    ZID = common_schemata.zidRequired
    eventID = common_schemata.eventIDRequired
    points = common_schemata.pointsRequired