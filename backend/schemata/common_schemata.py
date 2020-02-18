from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE

zid = fields.Str(required=True, validate=validate.Regexp('^[zZ][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', error='Malformed ZID'))

token = fields.Str(required=True, validate=validate.Regexp('^[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_]$', error='Malformed Token'))

name = fields.Str(required=True, validate=validate.Length(min=1, max=256))

eventID = fields.Str(required=True, validate=validate.Regexp('^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]([0-9][0-9][0-9][0-9][0-9]|)$'), error='Malformed EventID')