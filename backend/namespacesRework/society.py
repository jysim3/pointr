from flask_restx import Namespace, Resource, abort
from util.validation_services import validateArgsWith, validateWith
from util.auth_services import checkAuthorization
from schemata.soc_schemata import SocietyCreationScheme, SocietyIDSchema, SocietyPatchSchema
from schemata.models import authModel

api = Namespace('soc', description='Society Attendance Services')

from app import db
from flask import jsonify

"""
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
"""

@api.route('')
class Society(Resource):

    @api.doc(description='''
        Get the society described by the given socID
        <h4> Authorization Detials: </h4>
        Requires a socMember
    ''')
    @api.expect(authModel)
    @validateArgsWith(SocietyIDSchema)
    #@checkAuthorization()
    def get(self, argsData):
        return jsonify({"status": "success", "data": [argsData.getSocietyJSON()]})

    @api.doc(description='''
        Make a society using the given data
        <h4> Authorization Details: </h4>
        Requires a superadmin
    ''')
    #@checkAuthorization(level=2)
    @api.expect(authModel)
    @validateWith(SocietyCreationScheme)
    def post(self, data):
        db.session.add(data)
        db.session.commit()

        return jsonify({"status": "success", "data": [{"id": data.id}]})

    @api.doc(description='''
        Update a society using the given data
        <h4> Authorization Details: </h4>
        Requires a superadmin
    ''')
    @api.expect(authModel)
    @validateArgsWith(SocietyIDSchema)
    @validateWith(SocietyPatchSchema)
    #@checkAuthorization(allowSocAdmin=True)
    def patch(self, argsData, data):
        if argsData:
            for key, value in data.items():
                setattr(argsData,key,value)

            db.session.add(argsData)
            db.session.commit()

            return jsonify({"status": "success", "payload": [argsData.getSocietyJSON()]})
        else:
            abort(400, "Invalid eventID")
    
    @api.doc(description='''
        Get the society described by the given socID
        <h4> Authorization Detials: </h4>
        Requires a socMember
    ''')
    @api.expect(authModel)
    @validateArgsWith(SocietyIDSchema)
    #@checkAuthorization()
    def delete(self, argsData):
        db.session.delete(argsData)
        db.session.commit()

        return jsonify({"status": "success"})

@api.route('/tags')
class Tags(Resource):

    @api.doc(description='''
        Returns static list of all society tags possible
    ''')
    def get(self):
        pass

@api.route('/tag')
class Tag(Resource):

    @api.doc(description='''
        Returns preview of societies with the given tags (multiple tags are OR'd)
    ''')
    def get(self):
        pass

@api.route('/events/upcoming')
class Upcoming(Resource):

    @api.doc(description='''
        Returns previews of upcoming events of society
    ''')
    def get(self):
        pass

@api.route('/events/past')
class Past(Resource):

    @api.doc(description='''
        Returns previews of past events of society
    ''')
    def get(self):
        pass

@api.route('/admin')
class Admin(Resource):

    def post(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass