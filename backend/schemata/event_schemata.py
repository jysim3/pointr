from marshmallow import Schema, fields, ValidationError, validates, validate, post_load, EXCLUDE, validates_schema
from models.event import CompositeEvent, Event
from flask import abort
from schemata import common_schemata
import constants as c
from constants import PUBLIC
import uuid
import random
from string import ascii_uppercase, digits
from datetime import datetime
import pytz

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
    privacy = fields.Int(missing=PUBLIC, 
                         default=PUBLIC, 
                         validate=validate.Range(0, len(c.EVENT_STATUS)))
    tags = fields.List(fields.Int(validate=validate.Range(0, len(c.EVENT_TAGS))), required=True)

    hasQR = fields.Boolean(required=True)
    hasAccessCode = fields.Boolean(required=True)
    hasAdminSignin = fields.Boolean(required=True)

    additionalInfo = fields.List(fields.Str())

    @post_load
    def makeEvent(self, data, **kwargs):
        data['id'] = ''.join(random.choices(ascii_uppercase + digits, k=5))
        #if data['start'] > data['end'] or min(data['end'], data['start']) < datetime.now(pytz.utc):
        if data['start'] > data['end'] or data['end'] < datetime.now(pytz.utc):
            abort(400, "Specified time not valid")
        return Event(**data)

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
    privacy = fields.Int(validate=validate.Range(0, len(c.EVENT_STATUS)))
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
        if not data['code'].lower() in event.getAttendCodes():
            raise ValidationError("Attend code invalid or expired", "code")

    class Meta:
        unknown = EXCLUDE
    
class EventNumberSchema(Schema):
    number = fields.Int()

class EventPhotoSchema(Schema):
    photo = fields.Raw(required=True)