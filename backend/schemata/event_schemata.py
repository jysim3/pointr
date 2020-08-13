from marshmallow import Schema, fields, ValidationError, validates, validate, post_load, EXCLUDE, validates_schema
from models.event import CompositeEvent, Event
from flask import abort
from schemata import common_schemata
from constants import constants as c
import uuid
import random
from string import ascii_uppercase, digits

class EventCreationSchema(Schema):
    __schema_name__ = "Event Form"

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
        data['id'] = ''.join(random.choices(ascii_uppercase + digits, k=5))
        return Event(**data)

    @validates('tags')
    def validateLength(self, value):
        if len(value) < 1:
            raise ValidationError('Requires at least one tag')

class EventJSONSchema(Schema):
    __schema_name__ = "Event JSON Form For Additional Information"

    question = common_schemata.questionsRequired

class EventJSONAttendanceSchema(Schema):
    __schema_name__ = "Event JSON Form For Additional Information"

    question = common_schemata.questionsRequired
    answer = common_schemata.answersRequired

class EventPatchSchema(Schema):
    __schema_name__ = "Event Patch Form"

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

class EventIDSchema(Schema):
    __schema_name__ = "Event ID Form"

    eventID = common_schemata.eventIDRequired

    class Meta:
        unknown = EXCLUDE

    @post_load
    def getEvent(self, data, **kwargs):
        
        event = Event.getEvent(data['eventID'])

        if not event:
            abort(400, {'eventID': ['That Event ID does not exist']})
        return event

class EventAttendCodeSchema(Schema):
    __schema_name__ = "Event Attend Code"
    code = fields.Str(required=True, validate=validate.Length(equal=5))
    eventID = fields.Str(required=True)

    @validates_schema
    def validate_code(self, data, **kwargs):
        event = Event.getEvent(data['eventID'])
        print(event.getAttendCodes())
        if not data['code'] in event.getAttendCodes():
            abort(400, "Attend code invalid or expired")

    class Meta:
        unknown = EXCLUDE
    
class EventNumberSchema(Schema):
    number = fields.Int()