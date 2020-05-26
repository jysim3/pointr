from marshmallow import Schema, fields, ValidationError, validates, validate, post_load
from models.event import CompositeEvent, Event
from flask import abort
from schemata import common_schemata
from constants import constants as c
import uuid

class EventCreationSchema(Schema):
    name = "Event Form"

    name = common_schemata.nameRequired
    start = common_schemata.dateRequired
    end = common_schemata.dateRequired

    # TODO photos = db.Column(db.ARRAY(db.Text), nullable=True)
    description = fields.Str(default="No Description")
    previewDescription = fields.Str(default="No Description")
    location = fields.Str(required=True)

    status = fields.Int(missing=c.EVENT_STATUS_DEFAULT, default=c.EVENT_STATUS_DEFAULT, validate=validate.Range(0, len(c.EVENT_STATUS)))
    tags = fields.List(fields.Int(validate=validate.Range(0, len(c.EVENT_TAGS))), required=True)

    hasQR = fields.Boolean(required=True)
    hasAccessCode = fields.Boolean(required=True)
    hasAdminSignin = fields.Boolean(required=True)

    @post_load
    def makeEvent(self, data, **kwargs):
        data['id'] = uuid.uuid4().hex
        return Event(**data)

    @validates('tags')
    def validateLength(self, value):
        if len(value) < 1:
            raise ValidationError('Requires at least one tag')
    
class EventPatchSchema(Schema):
    name = "Event Patch Form"

    name = common_schemata.name
    start = common_schemata.date
    end = common_schemata.date

    # TODO photos = db.Column(db.ARRAY(db.Text), nullable=True)
    description = fields.Str()
    previewDescription = fields.Str()
    location = fields.Str()

    status = fields.Int(validate=validate.Range(0, len(c.EVENT_STATUS)))
    tags = fields.List(fields.Int(validate=validate.Range(0, len(c.EVENT_TAGS))))

    hasQR = fields.Boolean()
    hasAccessCode = fields.Boolean()
    hasAdminSignin = fields.Boolean()

class RecurringEventSchema(Schema):
    pass
    #endDate = common_schemata.dateRequired
    #recurType = fields.Str(required=True, validate=validate.Regexp('^day$|^week$|^month$'), error='Must be one of [day, week, month]')
    #recurInterval = fields.Int(required=True, validate=validate.Range(min=1, max=365), error='Must be more than 1 and less than 365')

class EventIDSchema(Schema):
    eventID = common_schemata.eventIDRequired

    @post_load
    def makeEvent(self, data, **kwargs):
        
        data['eventID'] = data['eventID'].hex
        event = Event.getEvent(data['eventID'])

        if not event:
            abort(400, {'eventID': ['That Event ID does not exist']})
        return event
    
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