from marshmallow import Schema, fields, ValidationError, validates, validate
from schemata import common_schemata

# { zID: "z5214808", name: "Coffee Night", eventDate: "2019-11-19"}
class EventCreationSchema(Schema):
    pass
    #zID = common_schemata.zid
    #name = common_schemata.name
    #eventStartDate = common_schemata.dateRequired
    #eventEndDate = common_schemata.dateRequired
    #eventStartTime = common_schemata.timeRequired
    #eventEndTime = common_schemata.timeRequired
    
class RecurringEventSchema(Schema):
    pass
    #endDate = common_schemata.dateRequired
    #recurType = fields.Str(required=True, validate=validate.Regexp('^day$|^week$|^month$'), error='Must be one of [day, week, month]')
    #recurInterval = fields.Int(required=True, validate=validate.Range(min=1, max=365), error='Must be more than 1 and less than 365')

class EventIDSchema(Schema):
    eventID = common_schemata.eventID
    
class AttendSchema(Schema):
    eventID = common_schemata.eventIDRequired
    zID = common_schemata.zid

pos = fields.Int(default=0, validate=validate.Length(min=0))
pos.description = "Position from start"

number = fields.Int(default=1, validate=validate.Length(min=1))
number.description = "Number from position"

class OffsetSchema(Schema):
    name = "Search Offset"
    pos = pos
    number = number