from marshmallow import Schema, fields, ValidationError, validates, validate
from schemata.common_schemata import name, zid

# { zID: "z5214808", name: "Coffee Night", eventDate: "2019-11-19"}
class EventCreationSchema(Schema):
    zID = zid
    name = name
    eventDate = fields.DateTime(required=True)
    eventStart = fields.DateTime()
    eventEnd = fields.DateTime()

class EventIDSchema(Schema):
    eventID = fields.Str(required=True, validate=validate.Length(equal=5))