from marshmallow import Schema, fields, ValidationError, validates, validate, post_load
from schemata import common_schemata
from models.user import Users

class ZIDSchema(Schema):
    zID = common_schemata.zidRequired

class ZIDSchemaNotReq(Schema):
    zID = common_schemata.zid

    @post_load
    def getUser(self, data, **kwargs):
        user = Users.findUser(data['zID'])
        return user if user else None

class DeletePointsSchema(Schema):
    ZID = common_schemata.zid
    eventID = common_schemata.eventIDRequired
    
class PostPointsSchema(Schema):
    ZID = common_schemata.zidRequired
    eventID = common_schemata.eventIDRequired
    points = common_schemata.pointsRequired