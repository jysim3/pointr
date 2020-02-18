from marshmallow import Schema, fields, ValidationError, validates, validate

# { zID: "z5214808", name: "Coffee Night", eventDate: "2019-11-19"}
class EventCreationSchema(Schema):
    zID = fields.Str(required=True, validate=validate.Length(equal=8))
    name = fields.Str(required=True)
    eventDate = fields.DateTime(required=True)
    eventStart = fields.DateTime()
    eventEnd = fields.DateTime()

class EventIDSchema(Schema):
    eventID = fields.Str(required=True, validate=validate.Length(equal=5))