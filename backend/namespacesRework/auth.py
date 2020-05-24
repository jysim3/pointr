from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, fields
from util.validation_services import toModel, validateWith, validateArgsWith
from schemata.auth_schemata import RegisterDetailsSchema, LoginDetailsSchema, TokenSchema, ZIDDetailsSchema, PasswordSchema
from schemata.models import authModel
from util import auth_services

api = Namespace('rework/auth', description='Authentication & Authorization Services Rework')

@api.route('/register')
class Register(Resource):
    
    @api.doc(description='''
        Registers a user, sends an email to the specified student's university email
        with a token to activate that needs to be sent to `/api/auth/activate`
    ''')
    @api.expect(toModel(api, RegisterDetailsSchema))
    @validateWith(RegisterDetailsSchema)
    def post(self, data):
        pass

@api.route('/login')
class Login(Resource):
    
    @api.doc(description='''
        Authorizes a user and returns a timestamped token
    ''')
    @api.expect(toModel(api, LoginDetailsSchema))
    @validateWith(LoginDetailsSchema)
    def post(self, data):
        pass

@api.route('/activate')
class Activate(Resource):

    @api.doc(description='''
        Takes token that was emailed to student when they registered using `/api/auth/register` 
        and now gives them 'activated' status from now on.      
    ''')
    @api.expect(authModel)
    @auth_services.check_authorization(activationRequired=False, level=0)
    def post(self, token_data):
        pass

@api.route('/forgot')
class Forgot(Resource):

    @api.doc(description='''
        Sends an email to the given zIDs student email with a temporary token that can be used in
        `/api/auth/reset` to reset the password
    ''')
    @api.expect(toModel(api, ZIDDetailsSchema))
    @validateWith(ZIDDetailsSchema)
    def post(self, data):
        pass
        
@api.route('/reset')
class Reset(Resource):
    
    @api.doc(description='''
        Takes a token in the header that was generated in `/api/auth/forgot` and emailed
        to the student
        Expects new password in body
    ''')
    @api.expect(toModel(api, PasswordSchema), authModel)
    @auth_services.check_authorization(level=0, activationRequired=False)
    @validateWith(PasswordSchema)
    def post(self, token_data, data):
        pass

@api.route('/change')
class changePassword(Resource):

    @api.doc(description='''
        Takes in a password for the user 
        TODO should probably also take old password
    ''')
    @api.expect(toModel(api, PasswordSchema), authModel)
    @auth_services.check_authorization(level = 1)
    @validateWith(PasswordSchema)
    def post(self, token_data):
        pass

@api.route('/validate')
@api.param('token', description='User Token', type='String', required='True')
class Authorize(Resource):

    @api.doc(description='''
        Status 200 if valid token
    ''')
    @api.expect(authModel)
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        return jsonify({"valid" : "true"})

# Validation functions To be removed
@api.route('/validateSelf')
@api.param('token', description='User Token', type='String', required='True', location='headers')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(activationRequired=False, level=5, allowSelf=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})

@api.route('/validateSocietyAdmin')
@api.param('token', description='User Token', type='String', required='True')
@api.param('societyID', description='Society ID', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(level=5, allowSocStaff=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})
        
@api.route('/validateEventAdmin')
@api.param('token', description='User Token', type='String', required='True')
@api.param('eventID', description='Event ID', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(level=5, allowSocStaff=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})
