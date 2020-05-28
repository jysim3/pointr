from flask import request, jsonify, send_from_directory, send_file, abort
from flask_restx import Namespace, Resource
from util import auth_services

api = Namespace('user', description='Reworked User Services')

from app import db
from models.user import Users
from util.validation_services import validateArgsWith, validateWith
from schemata.user_schemata import ZIDSchema, ZIDSchemaNotReq, zIDPatchSchema
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
    @validateWith(zIDPatchSchema)
    @checkAuthorization(allowSelf=True)
    def patch(self, token_data, data):
        user = Users.query.filter_by(zID=token_data['zID']).first()

        for key,value in data.items():
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
        Get events (in preview JSON format) visible to token bearer, i.e. the events he has attended
        the amount of events shown can be specified in args
    ''')
    @checkAuthorization()
    def get(self, token_data):
        user = Users.findUser(token_data['zID'])
        socs = user.getSocs(json=True)

        return jsonify({'status': 'success', 'data': socs})