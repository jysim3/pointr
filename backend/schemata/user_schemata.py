from marshmallow import Schema, fields, ValidationError, validates, validate, post_load, EXCLUDE
from schemata import common_schemata
from models.user import Users
from werkzeug import FileStorage

class ZIDSchema(Schema):
    __schema_name__ = "ZID form"
    zID = common_schemata.zidRequired

    class Meta:
        unknown = EXCLUDE

    @post_load
    def makeUser(self, data, **kwargs):
        return Users.findUser(data['zID'])

class ZIDSchemaNotReq(Schema):
    zID = common_schemata.zid

    @post_load
    def getUser(self, data, **kwargs):
        user = Users.findUser(data['zID'])
        return user if user else None

class zIDPatchSchema(Schema):
    password = common_schemata.password
    firstName = common_schemata.name
    lastName = common_schemata.name
    preferredName = common_schemata.name

    description = fields.Str()

    school = fields.Int()
    faculty = fields.Int()
    degree = fields.Int()
    commencementYear = common_schemata.commencementYear