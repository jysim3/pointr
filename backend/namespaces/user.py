from flask import request, jsonify, send_from_directory, send_file, abort
from flask_restx import Namespace, Resource
from util import auth_services

api = Namespace('user', description='Reworked User Services')

from app import db
from models.user import Users
from util.validation_services import toQuery, toModel, validateArgs, validateBody
from schemata.user_schemata import ZIDSchema, ZIDSchemaNotReq, zIDPatchSchema
from schemata.models import authModel
from util.auth_services import checkAuthorization
from util.files import uploadImages
#from werkzeug import FileStorage

photoModel = api.parser()
photoModel.add_argument('photo', required=True, help="WERKZEUG'S FILESTORAGE ISNT WORKING SO STR IS A PLACEHOLDER", type=str, location="files")
photoModel.add_argument('zID', required=True, help="The user's profile to be changed", type=str, location="args")

@api.route('')
class User(Resource):

    @api.doc(description='''
        Get the information regarding the user (i.e. name, photo, etc. But no events/soc info)
        Everybody's profile is public
    ''')
    @validateArgs(ZIDSchemaNotReq, 'user')
    @checkAuthorization(onlyAllowSelf=True, activationRequired=False)
    def get(self, token_data, user):
        return jsonify({'status': 'success', 'data': user.getJSON()})

    @api.doc(description='''
        Update the token-bearer's information
    ''')
    @validateBody(zIDPatchSchema, 'patchData')
    @checkAuthorization(allowSelf=True)
    def patch(self, token_data, patchData):
        user = Users.query.filter_by(zID=token_data['zID']).first()

        for key,value in patchData.items():
            setattr(user,key,value)

        db.session.add(user)
        db.session.commit()
        return jsonify({'status': 'success', 'data': user.getJSON()})
    
    @api.doc(description='''
        Delete the token-bearer
    ''')
    @checkAuthorization(allowSelf=True)
    def delete(self, token_data):
        user = Users.query.filter_by(zID=token_data['zID']).first()

        db.session.delete(user)
        db.session.commit()

        return jsonify({'status': 'success'})

@api.route('/photo')
class ProfilePhoto(Resource):

    @api.doc(description='''
        Update the token bearer's profile photo, alternatively, update someone else's
        profile photo if the token bearer is a superadmin.

        NOTE: Requires the zID of the profile to be changed for both token bearer update
        and superadmin update
    ''')
    @api.expect(photoModel)
    @validateArgs(ZIDSchema, 'user')
    @checkAuthorization(allowSelf=True, allowSuperAdmin=True)
    def patch(self, token_data, user):
        if not user:
            abort(405, "No such user")

        photo = request.files['photo']
        if not photo:
            abort(400, "No photo provided")

        status = uploadImages(photo)
        if not isinstance(status, tuple):
            abort(400, status)

        user.updatePhoto(status[0])
        return jsonify({'status': 'success'})

@api.route('/events/upcoming')
class UpcomingEvents(Resource):

    @api.doc(description='''
        Get events (in preview JSON format) visible to token bearer coming up in the future, 
        the amount of events shown can be specified in args
    ''')
    @checkAuthorization()
    def get(self, token_data):
        # TODO: Use validateArgs to get the number 
        user = Users.findUser(token_data['zID'])
        events = user.getUpcomingJSONs()

        return jsonify({'status': 'success', 'data': events})
    
@api.route('/events/past')
class PastEvents(Resource):

    @api.doc(description='''
        Get events (in preview JSON format) visible to token bearer, i.e. the events he has attended
        the amount of events shown can be specified in args
    ''')
    @checkAuthorization()
    def get(self, token_data):
        user = Users.findUser(token_data['zID'])
        events = user.getPastJSONs()

        return jsonify({'status': 'success', 'data': events})

@api.route('/societies')
class Societies(Resource):

    @api.doc(description='''
        Get a list of all society JSONs that this user is a part of
    ''')
    @checkAuthorization()
    def get(self, token_data):
        user = Users.findUser(token_data['zID'])
        socs = user.getSocs(json=True)

        return jsonify({'status': 'success', 'data': socs})