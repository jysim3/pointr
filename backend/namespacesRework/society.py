from flask_restx import Namespace, Resource
from util.validation_services import validateArgsWith, validateWith, validateBody, validateArgs
from util.auth_services import checkAuthorization
from schemata.soc_schemata import *
from schemata.models import authModel
from constants import constants

api = Namespace('rework/soc', description='Society Attendance Services')

from app import db
from flask import jsonify, abort
from models.user import Users

@api.route('')
class Society(Resource):

    @api.doc(description='''
        Get the society described by the given socID
        <h4> Authorization Detials: </h4>
        Requires a socMember
    ''')
    @api.expect(authModel)
    @validateArgs(SocietyIDSchema, 'society')
    #@checkAuthorization()
    def get(self, society):
        return jsonify({"status": "success", "data": society.getSocietyJSON()})

    @api.doc(description='''
        Make a society using the given data
        <h4> Authorization Details: </h4>
        Requires a superadmin
    ''')
    #@checkAuthorization(level=2)
    @api.expect(authModel)
    @validateBody(SocietyCreationScheme, 'society')
    def post(self, society):
        db.session.add(society)
        db.session.commit()

        return jsonify({"status": "success", "data": {"id": society.id}})

    @api.doc(description='''
        Update a society using the given data
        <h4> Authorization Details: </h4>
        Requires a superadmin
    ''')
    @api.expect(authModel)
    @validateArgs(SocietyIDSchema, 'society')
    @validateBody(SocietyPatchSchema, 'patchData')
    #@checkAuthorization(allowSocAdmin=True)
    def patch(self, society, patchData):

        for key,value in patchData.items():
            setattr(society,key,value)

        db.session.add(society)
        db.session.commit()

        return jsonify({"status": "success", "data": society.getSocietyJSON()})
    
    @api.doc(description='''
        Get the society described by the given socID
        <h4> Authorization Detials: </h4>
        Requires a socMember
    ''')
    @api.expect(authModel)
    @validateArgs(SocietyIDSchema, 'society')
    #@checkAuthorization()
    def delete(self, society):
        db.session.delete(society)
        db.session.commit()

        return jsonify({"status": "success"})

@api.route('/join')
class Join(Resource):
    @validateArgsWith(SocietyIDSchema)
    @checkAuthorization()
    def post(self, token_data, argsData):
        # FIXME: WE NEED TO CHECK WHETHER OR NOT THIS SOCIETY ALLOWS PEOPLE TO JOIN
        user = Users.query.filter_by(zID=token_data['zID']).first()
        status = argsData.addStaff(user)
        if status:
            abort(405, f"Invalid Parametres {status}")

        return jsonify({'status': 'success'})

@api.route('/leave')
class Leave(Resource):
    @validateArgs(SocietyIDSchema, 'society')
    @checkAuthorization(allowSocMember=True)
    def post(self, token_data, society):
        user = Users.query.filter_by(zID=token_data['zID']).first()
 
        status = society.deleteStaff(user)
        if status:
            abort(405, status)

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

    @api.doc(description='''
        Promotes a soc member to a given rank, requires a socAdmin account bearer
        for that society
        <h4> Authorization Details: </h4>
        Requires a socAdmin
    ''')
    @validateBody(SocietyIDSchema, 'society')
    @validateBody(SocietyRankSchema, 'rank')
    @validateBody(ZIDSchema, 'user')
    @checkAuthorization(allowSocAdmin=True)
    def post(self, society, rank, user, token_data):
        if not society:
            abort(403, "Invalid Parameters, no such society")

        status = society.addStaff(user, rank)
        if status:
            abort(405, status)

        return jsonify({'status': 'success'})

    @api.doc(description='''
        Returns a list of all admins of a given society
    ''')
    @validateBody(SocietyIDSchema, 'society')
    @checkAuthorization()
    def get(self, token_data, society):
        if not society:
            abort(403, "Invalid Parameters, no such society")

        return jsonify({'status': 'success', 'data': society.getAdmins()})

    @api.doc(description='''
        Demotes a soc member to a given rank (or remove from society if a rank is not specified), 
        requires a socAdmin account bearer for that society
        <h4> Authorization Details: </h4>
        Requires a socAdmin
    ''')
    @validateBody(SocietyIDSchema, 'society')
    @validateBody(SocietyRankSchema, 'rank')
    @validateBody(ZIDSchema, 'user')
    @checkAuthorization(allowSocAdmin=True)
    def delete(self, token_data, society, rank, user):
        if not society:
            abort(403, "Invalid Parameters, no such society")

        status = society.deleteStaff(user, rank)
        if status:
            abort(405, status)

        return jsonify({'status': 'success'})