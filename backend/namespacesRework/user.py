from flask import request, jsonify, send_from_directory, send_file
from flask_restx import Namespace, Resource, abort
from util import auth_services

api = Namespace('rework/user', description='Reworked User Services')

from app import db
from models.user import Users
from util.validation_services import validateArgsWith, validateWith
from schemata.user_schemata import ZIDSchema, ZIDSchemaNotReq
from util.auth_services import checkAuthorization

@api.route('')
class User(Resource):

    @api.doc(description='''
        Get the information regarding the user (i.e. name, photo, etc. But no events/soc info)
        Everybody's profile is public
    ''')
    # FIXME: Might change the publicity of profiles later on
    @validateArgsWith(ZIDSchemaNotReq)
    #@checkAuthorization()
    def get(self, argsData):
        return jsonify({'status': 'success', 'data': argsData.getJSON()})

    @api.doc(description='''
        Update the token-bearer's information
    ''')
    def patch(self):
        pass
    
    def delete(self):
        pass

@api.route('/events/upcoming')
class UpcomingEvents(Resource):

    def get(self):
        pass
    
@api.route('/events/past')
class PastEvents(Resource):

    def get(self):
        pass

@api.route('/societies')
class Societies(Resource):

    def get(self):
        pass