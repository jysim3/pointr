from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE, post_load, pre_load
from schemata import common_schemata
import constants as c
from constants import SOCIETY_TYPE
from uuid import uuid4
from models.society import Societies
from flask import abort
from models.user import Users

class SocietyIDSchema(Schema):
    __schema_name__ = "SocietyID Form"
    societyID = common_schemata.societyIDRequired

    class Meta:
        unknown = EXCLUDE

    @post_load
    def getSoc(self, data, **kwargs):
        data['societyID'] = data['societyID'].hex
        society = Societies.findSociety(data['societyID'])

        if not society:
            abort(400, {'societyID': ['That Society ID does not exist']})
        return society

class SocietyCreationSchema(Schema):
    __schema_name__ = "Society Form"

    name = common_schemata.nameRequired

    description = fields.Str(missing="No Description", default="No Description")
    previewDescription = fields.Str(missing="No Description", default="No Description")

    type = fields.Int(required=True)

    tags = fields.List(fields.Int(validate=validate.Range(0, len(c.EVENT_TAGS))), required=True)

    @post_load
    def makeSoc(self, data, **kwargs):

        if Societies.getSocietyByName(data['name']):
            abort(400, {'name': 'A society with that name already exists.'})

        data['id'] = uuid4().hex
        return Societies(**data)

class SocietyPatchSchema(Schema):
    __schema_name__ = "Society Patch Form"

    name = common_schemata.name

    description = fields.Str()
    previewDescription = fields.Str()

    type = fields.Int()

    tags = fields.List(fields.Int(validate=validate.Range(0, len(c.EVENT_TAGS))))

class SocietyTagSchema(Schema):
    tag = fields.Int()

class SocietyRankSchema(Schema):
    rank = fields.Int(validate=validate.Range(0, 5))

    class Meta:
        unknown = EXCLUDE

class SocietyLogoSchema(Schema):
    logo = fields.Raw(required=True)