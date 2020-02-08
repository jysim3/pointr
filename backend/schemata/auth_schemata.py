from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE
import jwt

class LoginDetailsSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=256))

class TokenSchema(Schema):
    token = fields.Str(required=True)
    
    class Meta():
        unknown = EXCLUDE