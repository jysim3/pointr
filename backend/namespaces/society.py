from flask_restx import Namespace, Resource
from util.validation_services import toQuery, toModel, validateArgs, validateBody
from util.auth_services import checkAuthorization
from schemata.soc_schemata import *
from schemata.user_schemata import ZIDSchema
from schemata.models import authModel
from constants import constants

api = Namespace('society', description='Society Attendance Services')

from app import db
from flask import jsonify, abort, request
from models.user import Users
from util.files import uploadImages

@api.route('')
class Society(Resource):

    @api.doc(description='''
        Get the society described by the given socID
        <h4> Authorization Detials: </h4>
        Requires a socMember
    ''')
    @api.expect(authModel)
    @validateArgs(SocietyIDSchema, 'society')
    @api.expect(authModel, toModel(api, SocietyIDSchema))
    #@checkAuthorization()
    def get(self, society):
        return jsonify({"status": "success", "data": society.getSocietyJSON()})

    @api.doc(description='''
        Make a society using the given data
        <h4> Authorization Details: </h4>
        Requires a superadmin
    ''')
    #@checkAuthorization(level=2)
    @api.expect(authModel, toModel(api, SocietyCreationSchema))
    @validateBody(SocietyCreationSchema, 'society')
    def post(self, society):
        db.session.add(society)
        db.session.commit()

        return jsonify({"status": "success", "data": {"id": society.id}})

    @api.doc(description='''
        Update a society using the given data
        <h4> Authorization Details: </h4>
        Requires a superadmin
    ''')
    @api.expect(authModel, toModel(api, SocietyPatchSchema))
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

@api.route('/logo')
class SocLogo(Resource):
    @api.doc(description='''
        Get the photo path of the soc logo provided by the query string
    ''')
    @api.expect(authModel)
    @validateArgs(SocietyIDSchema, 'society')
    def get(self, society):
        logo = society.getLogo()
        if not logo:
            abort(403, "No logo has been uploaded for this society")

        return jsonify({'status': 'success', 'data': logo})

    @api.doc(description='''
        Upload a new logo for the soc specified by the query string 
    ''')
    @api.expect(authModel)
    @validateArgs(SocietyIDSchema, 'society')
    def patch(self, society):
        if not request.files:
            abort(400, "Missing Parametres (no logo supplied)")

        status = uploadImages(request.files['logo'])
        if not isinstance(status, tuple):
            abort(403, status)

        society.setLogo(status[0])
        return jsonify({'status': 'success'})

    @api.doc(description='''
        Delete the logo of the soc specified by the query string
    ''')
    @api.expect(authModel)
    @validateArgs(SocietyIDSchema, 'society')
    def delete(self, society):
        logo = society.removeLogo()

        return jsonify({'status': 'success'})

@api.route('/join')
class Join(Resource):
    @checkAuthorization()
    @validateArgs(SocietyIDSchema, 'society')
    def post(self, token_data, society):
        # FIXME: WE NEED TO CHECK WHETHER OR NOT THIS SOCIETY ALLOWS PEOPLE TO JOIN
        user = Users.query.filter_by(zID=token_data['zID']).first()
        status = society.addStaff(user)
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
    @validateArgs(SocietyTagSchema, 'tags')
    @api.expect(authModel)
    #@checkAuthorization()
    def get(self, tags):
        socs = Societies.getSocietiesByTag(tags['tag'])
        socs = [i.getSocietyJSON() for i in socs]
        return jsonify({"status": "success", "data": socs})

@api.route('/events/upcoming')
class Upcoming(Resource):

    @api.doc(description='''
        Returns previews of upcoming events of society
    ''')
    @validateArgs(SocietyIDSchema, 'society')
    @api.expect(authModel)
    def get(self, society):
        events = society.getUpcomingEvents()
        events = [i.getPreview() for i in events]
        return jsonify({"status": "success", "data": events})

@api.route('/events/past')
class Past(Resource):

    @api.doc(description='''
        Returns previews of past events of society
    ''')
    @validateArgs(SocietyIDSchema, 'society')
    @api.expect(authModel)
    def get(self, society):
        events = society.getPastEvents()
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