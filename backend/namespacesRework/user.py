from flask import request, jsonify, send_from_directory, send_file
from flask_restx import Namespace, Resource, abort
from util import auth_services

api = Namespace('rework/user', description='Reworked User Services')

@api.route('')
class User(Resource):

    def get(self):
        pass

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