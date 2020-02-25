from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE

zid = fields.Str(validate=validate.Regexp('^[zZ][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', error='Malformed ZID'))

commencementYear = fields.Str(validate=validate.Regexp('^20[0-2][0-9]$', error='Bad Year'))

registrationType = fields.Str(required=False, validate=validate.Length(min = 1, max = 25))

zidRequired = fields.Str(required=True, validate=validate.Regexp('^[zZ][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', error='Malformed ZID'))

token = fields.Str(validate=validate.Regexp('^[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_-]*$', error='Malformed Token'))

tokenRequired = fields.Str(required=True, validate=validate.Regexp('^[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_-]*$', error='Malformed Token'))

name = fields.Str(required=True, validate=validate.Length(min=1, max=256))

eventID = fields.Str(validate=validate.Regexp('^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]([0-9][0-9][0-9][0-9][0-9]|)$'), error='Malformed EventID')

eventIDRequired = fields.Str(required=True, validate=validate.Regexp('^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]([0-9][0-9][0-9][0-9][0-9]|)$'), error='Malformed EventID')

societyID = fields.Str(error='Malformed societyID')

societyIDRequired = fields.Str(required=True, error='Malformed societyID')

password = fields.Str(required=True, validate=validate.Length(min=8, max=256), error="Enter a valid Password")

isArc = fields.Bool(required=True, error="Not a boolean")