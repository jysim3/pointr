from flask import request, jsonify, send_file
from flask_restx import Namespace, Resource, abort
from util.validation_services import validateArgsWith, validateWith, toQuery
from util.validation_services import toModel
from schemata.event_schemata import AttendSchema, EventCreationSchema, EventPatchSchema
from util import auth_services
from schemata.models import authModel, offsetModel
from schemata.event_schemata import OffsetSchema, EventIDSchema
from pprint import pprint
from app import db
from models.event import Event
api = Namespace('rework/event', description='Reworked Event Management Services')

@api.route('')
class EventRoute(Resource):
    
    @api.doc(description='''
        Creates an event with data given body data for the society specified (as either query or in body)
        <h3>Authorization Details:</h3>
        Requires the token bearer to be an admin of one of the specified societies
    ''')
    #@api.expect(toModel(api, EventCreationSchema))
    #@auth_services.check_authorization(level=2, allowSocStaff=True)
    @validateWith(EventCreationSchema)
    def post(self, data):
        print("event.py" + str(data.start))
        db.session.add(data)
        db.session.commit()
        return jsonify({"id": data.id})
    
    @api.doc(description='''
        Get the event described by the given eventID
        <h3>Authorization Details:</h3>
        Only returns full list of attendees if super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to get')
    @api.expect(authModel)
    # @auth_services.check_authorization(level=1)
    @validateArgsWith(EventIDSchema)
    def get(self, argsData):
        if argsData:
            return argsData.getEventJSON()
        else:
            abort(400, "Invalid eventID")
    
    @api.doc(description='''
        Delete the event described by the given eventID. 
        <h3>Authorization Details:</h3>
        Requires the token bearer to be super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to remove')
    @api.expect(authModel)
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    def delete(self, token_data):
        #TODO
        pass
    
    @api.doc(description='''
        Updates the given event (eventID can be query or body) with the given data.
        <h3>Authorization Details:</h3>
        Requires the token bearer to be super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to update')
    @api.expect(authModel)
    @validateArgsWith(EventIDSchema)
    @validateWith(EventPatchSchema)
    # @auth_services.check_authorization(level=2, allowSocStaff=True)
    def patch(self, argsData, data):
        if argsData:

            for key,value in data.items():
                setattr(argsData,key,value)

            db.session.add(argsData)
            db.session.commit()

            return argsData.getEventJSON()
        else:
            abort(400, "Invalid eventID")
        

@api.route('/test')
class Test(Resource):

    def post(self):
        return {"method": "post"}

    def get(self):
        return {"method": "get"}

    def patch(self):
        return {"method": "patch"}

    def delete(self):
        return {"method": "delete"}
    
    def put(self):
        return {"method": "put"}

@api.route('/attend')
class AttendRoute(Resource):

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
class AttendAdminRoute(Resource):

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
class UpcomingRoute(Resource):

    @api.doc(description='''
        Get events visible to token bearer coming up in the next days amount of days from offset inclusive (0 = today) 
    ''')
    @api.expect(authModel, toQuery(api, OffsetSchema))
    @auth_services.check_authorization(level=1)
    def get(self, token_data):
        pass

@api.route('/composite')
class CompositeRoute(Resource):

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