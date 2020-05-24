from flask import request, jsonify, send_file
from flask_restx import Namespace, Resource, abort
from util.validation_services import validateArgsWith, validateWith, toQuery
from schemata.event_schemata import AttendSchema
from util import auth_services
from schemata.models import authModel, offsetModel
from schemata.event_schemata import OffsetSchema
api = Namespace('rework/event', description='Reworked Event Management Services')

@api.route('')
class Event(Resource):
    
    @api.doc(description='''
        Creates an event with data given body data for the society specified (as either query or in body)
        <h3>Authorization Details:</h3>
        Requires the token bearer to be an admin of one of the specified societies
    ''')
    @api.expect(authModel)
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    def post(self, token_data):
        pass
    
    @api.doc(description='''
        Get the event described by the given eventID
        <h3>Authorization Details:</h3>
        Only returns full list of attendees if super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to get')
    @api.expect(authModel)
    @auth_services.check_authorization(level=1)
    def get(self, token_data):
        pass
    
    @api.doc(description='''
        Delete the event described by the given eventID. 
        <h3>Authorization Details:</h3>
        Requires the token bearer to be super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to remove')
    @api.expect(authModel)
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    def delete(self, token_data):
        pass
    
    @api.doc(description='''
        Updates the given event (eventID can be query or body) with the given data.
        <h3>Authorization Details:</h3>
        Requires the token bearer to be super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to update')
    @api.expect(authModel)
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    def patch(self, token_data):
        pass

@api.route('/attend')
class Attend(Resource):

    @api.doc(description='''
        The token bearer is recorded as having attended the given eventID.
    ''')
    @api.expect(authModel)
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        pass

    @api.doc(description='''
        The token bearer is no longer recorded as having attended the given eventID.
    ''')
    @api.expect(authModel)
    @auth_services.check_authorization(level=1)
    def delete(self, token_data):
        pass

@api.route('/attend/admin')
class AttendAdmin(Resource):

    @api.doc(description='''
        If the token bearer is an admin of the event, the zID given is recorded as having 
        attended the event.
    ''')
    @api.expect(authModel)
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    def post(self, token_data):
        pass

    @api.doc(description='''
        If the token bearer is an admin of the event, the zID given is recorded as 
        no longer having attended the event.
    ''')
    @api.expect(authModel)
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    def delete(self, token_data):
        pass

@api.route('/upcoming')
class Upcoming(Resource):

    @api.doc(description='''
        Get events visible to token bearer coming up in the next days amount of days from offset inclusive (0 = today) 
    ''')
    @api.expect(authModel, toQuery(api, OffsetSchema))
    @auth_services.check_authorization(level=1)
    def get(self, token_data):
        pass

@api.route('/composite')
class Composite(Resource):

    @api.doc(description='''
        Requests that the event specified as subEvent becomes a event within the event specfied by eventID
        <h3>Authorization:</h3>
        The token bearer must be an admin of eventID
    ''')
    @api.expect(authModel)
    def post(self):
        pass

    @api.doc(description='''
        Requests that the event specified as subEvent becomes a event within the event specfied by eventID
        <h3>Authorization:</h3>
        The token bearer must be an admin of eventID
    ''')
    @api.expect(authModel)
    def get(self):
        pass

    @api.doc(description='''
        Accepts that the event specified as compositeEvent is now the container for eventID.
        <h3>Authorization:</h3>
        The token bearer must be an admin of eventID
    ''')
    @api.expect(authModel)
    def get(self):
        pass

    
    @api.doc(description='''
        Removes the composition connection between eventID and subEventID
        <h3>Authorization:</h3>
        The token bearer must be an admin of either eventID or subEventID
    ''')
    @api.expect(authModel)
    def delete(self):
        pass