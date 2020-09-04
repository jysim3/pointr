from flask import request, jsonify, send_file
from flask_restx import Namespace, Resource, abort
from util.validation_services import toQuery, toModel, validateArgs, validateBody
from schemata.event_schemata import EventCreationSchema, EventPatchSchema, EventAttendCodeSchema
from util import auth_services
from schemata.models import authModel, offsetModel
from schemata.event_schemata import EventIDSchema, EventNumberSchema, EventJSONSchema, EventJSONAttendanceSchema, EventPhotoSchema
from schemata.soc_schemata import SocietyIDSchema
from schemata.user_schemata import ZIDSchema
from pprint import pprint

api = Namespace('event', description='Reworked Event Management Services')

from util.auth_services import checkAuthorization
# from util.files import uploadImages
from app import db
from models.event import Event, Attendance
from models.user import Users
from datetime import datetime
from util.files import uploadImages

photoModel = api.parser()
photoModel.add_argument('photo', required=True, help="WERKZEUG'S FILESTORAGE ISNT WORKING SO STR IS A PLACEHOLDER", type=str, location="files")
photoModel.add_argument('eventID', required=True, help="The event's photo to be changed", type=str, location="args")

@api.route('')
class EventRoute(Resource):
    
    @api.doc(description='''
        Creates an event with data given body data for the society specified (as either query or in body)
        <h3>Authorization Details:</h3>
        Requires the token bearer to be an admin of one of the specified societies
    ''')
    @api.expect(toModel(api, EventCreationSchema))
    @auth_services.checkAuthorization(level=1)
    @validateArgs(SocietyIDSchema, 'society')
    @validateBody(EventCreationSchema, 'event')
    def post(self, token_data, event, society):

        # FIXME (Steven, 15/08/2020): This bit wouldn't work with a file upload
        # Need to change the request body from json request to forms
        if 'photo' in request.files:
            photo = request.files['photo']

            status = uploadImages(photo)
            if not isinstance(status, tuple):
                abort(400, status)

            event.updatePhoto(status[0])

        society.hosting.append(event)
        db.session.add(event)
        db.session.add(society)
        db.session.commit()

        return jsonify({"status": "success", "data": {"id": event.id}})
    
    @api.doc(description='''
        Get the event described by the given eventID
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

        # TODO (Steven 15/08/2020): Allow changing the photo associated with the photo

        return jsonify({"status": "success", "data": event.getEventJSON()})

@api.route("/photo")
class EventPhoto(Resource):
    @api.doc(description='''
        Upload a photo to the specified event in the query string
    ''')
    @api.expect(photoModel)
    @validateArgs(EventIDSchema, "event")
    # @checkAuthorization(level=1, allowSocAdmin=True)
    def post(self, event, *args, **kwargs):
        photo = request.files['photo']
        if not photo:
            abort(400, "No photo provided")

        status = uploadImages(photo)
        if not isinstance(status, tuple):
            abort(400, status)

        event.updatePhoto(status[0])
        return jsonify({'status': 'success'})

    @api.doc(description='''
        Update a photo to the specified event in the query string
    ''')
    @api.expect(photoModel)
    @validateArgs(EventIDSchema, "event")
    # @checkAuthorization(level=1, allowSocAdmin=True)
    def patch(self, event, *args, **kwargs):
        photo = request.files['photo']
        if not photo:
            abort(400, "No photo provided")

        status = uploadImages(photo)
        if not isinstance(status, tuple):
            abort(400, status)

        event.updatePhoto(status[0])
        return jsonify({'status': 'success'})

    @api.doc(description='''
        Delete the photo attached to this particular event
    ''')
    @validateArgs(EventIDSchema, "event")
    # @checkAuthorization(level=1, allowSocAdmin=True)
    def delete(self, token_data, *args, **kwargs):
        event.updatePhoto(None)

        return jsonify({'status': 'success'})

@api.route("/additional")
class AdditionalInfo(Resource):
    @api.doc(description='''
        Insert additional questions that events should ask their users to fill out (ONE AT A TIME)
    ''')
    @api.expect(authModel, toModel(api, EventJSONSchema), toModel(api, EventIDSchema))
    @validateBody(EventJSONSchema, 'additionalInfo')
    @validateArgs(EventIDSchema, "event")
    @checkAuthorization(level=1, allowSocAdmin=True)
    def post(self, additionalInfo, token_data, event):
        status = event.addAdditionalInfo(additionalInfo)

        if status:
            abort(400, status)

        return jsonify({'status': 'success'})

    @api.doc(description='''
        Update existing questions with new questions (USE THIS ROUTE TO FIX TYPOS AND SHIT)
        <h4> CURRENTLY NOT IMPLEMENTED </h4>
    ''')
    def patch(self):
        pass

    @api.doc(description='''
        Delete a previously set question for a particular event
    ''')
    @api.expect(authModel, toModel(api, EventJSONSchema), toModel(api, EventIDSchema))
    @validateBody(EventJSONSchema, 'additionalInfo')
    @validateArgs(EventIDSchema, "event")
    @checkAuthorization(level=1, allowSocAdmin=True)
    def delete(self, additionalInfo, token_data, event):
        status = event.deleteAdditionalInfo(additionalInfo)

        if status:
            abort(400, status)

        return jsonify({'status': 'success'})
        

@api.route('/attend/code')
class AttendCode(Resource):
    @api.doc(description='''
        Returns an attend code for the admin to display
    ''')
    @api.expect(authModel)
    @validateArgs(EventIDSchema, 'event')
    @checkAuthorization(level=1)
    def get(self, token_data, event):

        return jsonify({'status': 'success', 'data': event.getAttendCode()})
"""
FIXME: CHUCK ALL THIS INTO ARGS STRING, CHECK ARGS STRING, WORK ON VALIDATEARGSWITH
"""
@api.route('/attend')
class AttendRoute(Resource):

    @api.doc(description='''
        The token bearer is recorded as having attended the given eventID.
    ''')
    @api.expect(authModel)
    @validateArgs(EventIDSchema, 'event')
    @validateArgs(EventAttendCodeSchema, 'code')
    @checkAuthorization(level=1)
    def post(self, token_data, event, code):
        user = Users.findUser(token_data['zID'])
        status = event.addAttendance(user)
        if status:
            abort(403, status)
        return jsonify({"status": "success"})





    @api.doc(description='''
        The token bearer is no longer recorded as having attended the given eventID.
    ''')
    @api.expect(authModel)
    @validateArgs(ZIDSchema, 'user')
    @validateBody(EventIDSchema, 'event')
    @checkAuthorization(allowSocAdmin=True)
    #def delete(self, token_data, argsData, data):
    def delete(self, token_data, user, event):
        status = event.deleteAttendance(user)
        if status:
            abort(403, status)

        return jsonify({"status": "success"})

    @api.doc(description='''
        Get the list of people who attended this event in the format {zID, firstName, lastName, isArc, time}
    ''')
    @api.expect(authModel, toModel(api, EventIDSchema))
    @validateArgs(EventIDSchema, 'event')
    @checkAuthorization(allowSocAdmin=True, allowSuperAdmin=True)
    def get(self, token_data, event):
        return jsonify({'status': 'success', 'data': event.getAttendanceJSON()})

    @api.doc(description='''
        Update the attendace information of this particular user with answers to event specific questions
    ''')
    @checkAuthorization(allowSocMember=True)
    def patch(self, token_data):
        pass

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
    @api.expect(authModel)
    @validateArgs(EventNumberSchema)
    # NOTE: Do we want the public to see upcoming events as well?
    def get(self, argsData):
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