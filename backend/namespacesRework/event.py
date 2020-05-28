from flask import request, jsonify, send_file
from flask_restx import Namespace, Resource, abort
from util.validation_services import validateArgsWith, validateWith, toQuery, validateArgs, validateBody
from util.validation_services import toModel
from schemata.event_schemata import AttendSchema, EventCreationSchema, EventPatchSchema
from util import auth_services
from schemata.models import authModel, offsetModel
from schemata.event_schemata import OffsetSchema, EventIDSchema, EventNumberSchema
from schemata.soc_schemata import SocietyIDSchema, ZIDSchema, ZIDAndEventIDSchema
from pprint import pprint

api = Namespace('rework/event', description='Reworked Event Management Services')

from util.auth_services import checkAuthorization
from app import db
from models.event import Event, Attendance
from models.user import Users
from datetime import datetime
from pytz import timezone

@api.route('')
class EventRoute(Resource):
    
    @api.doc(description='''
        Creates an event with data given body data for the society specified (as either query or in body)
        <h3>Authorization Details:</h3>
        Requires the token bearer to be an admin of one of the specified societies
    ''')
    #@api.expect(toModel(api, EventCreationSchema))
    #@auth_services.check_authorization(level=2, allowSocStaff=True)
    @validateArgs(SocietyIDSchema, 'society')
    @validateBody(EventCreationSchema, 'event')
    def post(self, event, society):
        society.hosting.append(event)
        db.session.add(event)
        db.session.add(society)
        db.session.commit()

        return jsonify({"status": "success", "data": {"id": event.id}})
    
    @api.doc(description='''
        Get the event described by the given eventID
        <h3>Authorization Details:</h3>
        Only returns full list of attendees if super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to get')
    @api.expect(authModel)
    # @auth_services.check_authorization(level=1)
    @validateArgs(EventIDSchema, 'event')
    def get(self, event):
        return jsonify({"status": "success", "data": event.getEventJSON()})
    
    @api.doc(description='''
        Delete the event described by the given eventID. 
        <h3>Authorization Details:</h3>
        Requires the token bearer to be super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to remove')
    @api.expect(authModel)
    @validateArgs(EventIDSchema, 'event')
    def delete(self, event):
        
        Event.deleteEvent(event)

        return jsonify({"status": "success"})

    @api.doc(description='''
        Updates the given event (eventID can be query or body) with the given data.
        <h3>Authorization Details:</h3>
        Requires the token bearer to be super admin or admin of event
    ''')
    @api.param('eventID', 'The eventID of the event to update')
    @api.expect(authModel)
    @validateArgs(EventIDSchema, 'event')
    @validateBody(EventPatchSchema, 'patchData')
    # @auth_services.check_authorization(level=2, allowSocStaff=True)
    def patch(self, event, patchData):

        for key,value in patchData.items():
            setattr(event,key,value)

        db.session.add(event)
        db.session.commit()

        return jsonify({"status": "success", "data": event.getEventJSON()})
        

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

"""
FIXME: CHUCK ALL THIS INTO ARGS STRING, CHECK ARGS STRING, WORK ON VALIDATEARGSWITH
"""
@api.route('/attend')
class AttendRoute(Resource):

    @api.doc(description='''
        The token bearer is recorded as having attended the given eventID.
    ''')
    @api.expect(authModel)
    @validateArgsWith(EventIDSchema)
    @checkAuthorization(allowSocMember=True)
    def post(self, token_data, argsData):
        user = Users.findUser(token_data['zID'])
        status = argsData.addAttendance(user)
        if status:
            abort(405, status)

        return jsonify({"status": "success"})

    @api.doc(description='''
        The token bearer is no longer recorded as having attended the given eventID.
    ''')
    @api.expect(authModel)
    @validateArgsWith(ZIDSchema)
    @validateWith(EventIDSchema)
    #@checkAuthorization(allowSocAdmin=True)
    #def delete(self, token_data, argsData, data):
    def delete(self, argsData, data):
        status = data.deleteAttendance(argsData)
        if status:
            abort(405, status)

        return jsonify({"status": "success"})

@api.route('/attend/admin')
class AttendAdminRoute(Resource):

    @api.doc(description='''
        If the token bearer is an admin of the event, the zID given is recorded as having 
        attended the event.
    ''')
    @validateArgs(ZIDSchema, 'user')
    @validateArgs(EventIDSchema, 'event')
    @api.expect(authModel)
    @checkAuthorization(allowSocAdmin=True)
    def post(self, token_data, user, event):
        if not user or not event:
            abort(403, "Invalid Parameter, no such user or event")

        status = event.addAttendance(user)

        if status:
            abort(403, status)

        return jsonify({'status': 'success'})

    @api.doc(description='''
        If the token bearer is an admin of the event, the zID given is recorded as 
        no longer having attended the event.
    ''')
    @validateArgs(ZIDSchema, 'user')
    @validateArgs(EventIDSchema, 'event')
    @api.expect(authModel)
    @checkAuthorization(allowSocAdmin=True)
    def delete(self, token_data, user, event):
        if not user or not event:
            abort(403, "Invalid Parameter, no such user or event")

        status = event.deleteAttendance(user)

        if status:
            abort(403, status)

        return jsonify({'status': 'success'})

@api.route('/upcoming')
class UpcomingRoute(Resource):

    @api.doc(description='''
        Get an amount of all the upcoming events (amount specified in the query string)
    ''')
    @api.expect(authModel, toQuery(api, OffsetSchema))
    @validateArgsWith(EventNumberSchema)
    # NOTE: Do we want the public to see upcoming events as well?
    @checkAuthorization(level=1)
    def get(self, token_data, argsData):
        number = argsData['number'] if 'number' in argsData else 5
        return jsonify({'status': 'success', 'data': Event.getAllUpcomingEventsJSONs(number)})

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