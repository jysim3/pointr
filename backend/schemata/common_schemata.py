from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE

commencementYear = fields.Int(validate=validate.Range(min=2000, max=2030), error='Bad Year')

registrationType = fields.Str(required=False, validate=validate.Length(min = 1, max = 25))

zid = fields.Str(validate=validate.Regexp('^[zZ][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', error='Malformed ZID'))

zidRequired = fields.Str(required=True, validate=validate.Regexp('^[zZ][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', error='Malformed ZID'))

token = fields.Str(validate=validate.Regexp('^[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_-]*$', error='Malformed Token'))

tokenRequired = fields.Str(required=True, validate=validate.Regexp('^[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_-]*$', error='Malformed Token'))

name = fields.Str(required=True, validate=validate.Length(min=1, max=256))

eventID = fields.Str(validate=validate.Regexp('^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]([0-9][0-9]|)$'), error='Malformed EventID')

eventIDRequired = fields.Str(required=True, validate=validate.Regexp('^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]([0-9][0-9]|)$'), error='Malformed EventID')

societyID = fields.Str(error='Malformed societyID')

societyIDRequired = fields.Str(required=True, error='Malformed societyID')

password = fields.Str(validate=validate.Length(min=8, max=256), error="Enter a valid Password")

passwordRequired = fields.Str(required=True, validate=validate.Length(min=8, max=256), error="Enter a valid Password")

isArc = fields.Bool(required=True, error="Not a boolean")

date = fields.Str(validate=validate.Regexp('^202[0-9]-[0-1][0-9]-[0-3][0-9]$'))

dateRequired = fields.Str(required=True, validate=validate.Regexp('^202[0-9]-[0-1][0-9]-[0-3][0-9]$'))
