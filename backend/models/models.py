from flask_restx import fields as flask_fields
from init import api

event_details = api.model('event_details', {
    'z_id': flask_fields.String(required=True, example='z1234567'),
    'name': flask_fields.String(required=True, example='Coffe Night'),
    'event_date': flask_fields.DateTime()
})

event_id = api.model('event_id', {
    'eventID': flask_fields.String()
})

auth_details = api.model('auth_details', {
    'username': flask_fields.String(required=True, example='xX_greginator_Xx'),
    'password': flask_fields.String(required=True, example='1234')
})
    
token_details = api.model('token_details', {
    'token': flask_fields.String(required=True, example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Nzk4MzczNTcsImlhdCI6MTU3OTgzMzc1NywidXNlcm5hbWUiOiJhc2QifQ.LxzbjHUa0CxXH_z3_xZempr9gbTWqmUpM81oRd4gbkU')
})

token_check = api.model('token_check', {
    'valid': flask_fields.Boolean()
})