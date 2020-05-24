from marshmallow import Schema, fields, ValidationError, validates, validate, EXCLUDE
import datetime

commencementYearRequired = fields.Int(required=True, validate=validate.Range(min=2000, max=datetime.datetime.now().year), error='Enter a valid year')

zid = fields.Str(validate=validate.Regexp('^[zZ][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', error='Malformed ZID'))

zidRequired = fields.Str(required=True, validate=validate.Regexp('^[zZ][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', error='Malformed ZID'))
zidRequired.description = "zID of student in question"
zidRequired.example = "z12345678"

token = fields.Str(validate=validate.Regexp('^[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_-]*$', error='Malformed Token'))

tokenRequired = fields.Str(required=True, validate=validate.Regexp('^[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_]*\.[a-zA-Z0-9+_-]*$', error='Malformed Token'))

nameRequired = fields.Str(required=True, validate=validate.Length(min=1, max=256))

eventID = fields.Str(validate=validate.Regexp('^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]([0-9][0-9]|)$'), error='Malformed EventID')

eventIDRequired = fields.Str(required=True, validate=validate.Regexp('^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]([0-9][0-9]|)$'), error='Malformed EventID')

societyID = fields.Str(error='Malformed societyID')

societyIDRequired = fields.Str(required=True, error='Malformed societyID')

password = fields.Str(validate=validate.Length(min=8, max=256), error="Enter a valid Password")

passwordRequired = fields.Str(required=True, validate=validate.Length(min=8, max=256), error="Enter a valid Password")
passwordRequired.description = "Password between 8 and 256 characters"
passwordRequired.example = "password"

booleanRequired = fields.Bool(required=True, error="Not a boolean")

date = fields.Str(validate=validate.Regexp('^202[0-9]-[0-1][0-9]-[0-3][0-9]$'))

dateRequired = fields.Str(required=True, validate=validate.Regexp('^202[0-9]-[0-1][0-9]-[0-3][0-9]$'))

points = fields.Int(error='Enter a valid point value')

pointsRequired = fields.Int(required=True, error='Enter a valid point value')

schools = ["Computer Science and Engineering"]

schoolRequired = fields.Str(required=True, validate=validate.OneOf(schools))

faculties = ["Engineering"]

facultyRequired = fields.Str(required=True, validate=validate.OneOf(faculties))

degrees = ["Computer Science"]

degreeRequired = fields.Str(required=True, validate=validate.OneOf(degrees))

studentType = ["International", "Domestic"]
