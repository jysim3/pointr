from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE, post_load
from schemata import common_schemata
from constants import constants as c
from constants.constants import SOCIETY_TYPE
from uuid import uuid4
from models.society import Societies

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

    @post_load
    def getSoc(self, data, **kwargs):
        print(data)
        return Societies.findSociety(data['societyID'])

class SocietyIDAndZIDSchema(Schema):
    societyID = common_schemata.societyIDRequired
    zID = common_schemata.zidRequired
    
    class Meta:
        unknown = EXCLUDE

class SocietyCreationScheme(Schema):
    name = "Society Form"

    name = common_schemata.nameRequired

    description = fields.Str(missing="No Description", default="No Description")
    previewDescription = fields.Str(missing="No Description", default="No Description")

    type = fields.Int(required=True)

    tags = fields.List(fields.Int(validate=validate.Range(0, len(c.EVENT_TAGS))), required=True)

    @post_load
    def makeSoc(self, data, **kwargs):
        data['id'] = uuid4().hex
        return Societies(**data)

class SocietyPatchSchema(Schema):
    name = "Society Patch Form"

    name = common_schemata.name

    description = fields.Str(missing="No Description", default="No Description")
    previewDescription = fields.Str(missing="No Description", default="No Description")

    type = fields.Int()

    tags = fields.List(fields.Int(validate=validate.Range(0, len(c.EVENT_TAGS))))

class SocietyTagSchema(Schema):
    tag = fields.Int()