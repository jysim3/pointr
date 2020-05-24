from flask_restx import Namespace, Resource, abort
from util.validation_services import validateArgsWith, validateWith

api = Namespace('soc', description='Society Attendance Services')

@api.route('')
class Society(Resource):

    def get(self):
        pass

    def post(self):
        pass
    
    def patch(self):
        pass
    
    def delete(self):
        pass

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