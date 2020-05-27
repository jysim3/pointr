from flask_restx import Namespace, Resource, abort
from util.validation_services import validateArgsWith, validateWith
from util.auth_services import checkAuthorization
from schemata.soc_schemata import *
from schemata.models import authModel
from constants import constants

api = Namespace('soc', description='Society Attendance Services')

from app import db
from flask import jsonify
from models.user import Users

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
        return jsonify({"status": "success", "data": argsData.getSocietyJSON()})

    @api.doc(description='''
        Make a society using the given data
        <h4> Authorization Details: </h4>
        Requires a superadmin
    ''')
    #@checkAuthorization(level=2)
    @api.expect(authModel)
    @validateWith(SocietyCreationScheme)
    def post(self, data):
        print("asdsa")
        db.session.add(data)
        db.session.commit()

        return jsonify({"status": "success", "data": {"id": data.id}})

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

        for key,value in data.items():
            setattr(argsData,key,value)

        db.session.add(argsData)
        db.session.commit()

        return jsonify({"status": "success", "data": argsData.getSocietyJSON()})
    
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

@api.route('/join')
class Join(Resource):
    @validateArgsWith(SocietyIDSchema)
    @checkAuthorization()
    def post(self, token_data, argsData):
        user = Users.query.filter_by(zID=token_data['zID']).first()
        status = argsData.addStaff(user)
        if status:
            abort(405, f"Invalid Parametres {status}")

        return jsonify({'status': 'success'})

@api.route('/tags')
class Tags(Resource):

    @api.doc(description='''
        Returns static list of all society tags possible
    ''')
    def get(self):
        return jsonify({"status": "success", "data": [constants.SOCIETY_TAGS]})

@api.route('/tag')
class Tag(Resource):

    @api.doc(description='''
        Returns preview of societies with the given tags (multiple tags are OR'd)
    ''')
    @validateArgsWith(SocietyTagSchema)
    @api.expect(authModel)
    #@checkAuthorization()
    def get(self, argsData):
        socs = Societies.getSocietiesByTag(argsData['tag'])
        socs = [i.getSocietyJSON() for i in socs]
        return jsonify({"status": "success", "data": socs})

@api.route('/events/upcoming')
class Upcoming(Resource):

    @api.doc(description='''
        Returns previews of upcoming events of society
    ''')
    @validateArgsWith(SocietyIDSchema)
    @api.expect(authModel)
    def get(self, argsData):
        events = argsData.getUpcomingEvents()
        events = [i.getPreview() for i in events]
        return jsonify({"status": "success", "data": events})

@api.route('/events/past')
class Past(Resource):

    @api.doc(description='''
        Returns previews of past events of society
    ''')
    @validateArgsWith(SocietyIDSchema)
    @api.expect(authModel)
    def get(self, argsData):
        events = argsData.getPastEvents()
        events = [i.getPreview() for i in events]
        return jsonify({"status": "success", "data": events})

@api.route('/admin')
class Admin(Resource):

    def post(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass