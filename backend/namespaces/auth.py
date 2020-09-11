from flask import request, jsonify, abort
from flask_restx import Namespace, Resource, fields
from util.validation_services import toQuery, toModel, validateArgs, validateBody
from schemata.auth_schemata import RegisterDetailsSchema, LoginDetailsSchema, TokenSchema, ZIDDetailsSchema, PasswordSchema, ChangePasswordSchema
from schemata.user_schemata import ZIDSchema
from schemata.models import authModel
from util import auth_services

api = Namespace('auth', description='Authentication & Authorization Services Rework')

from app import db
from models.user import Users
from util.auth_services import generateLoginToken, generateActivationToken, generateForgotToken
from util.emailPointr import sendActivationEmail, sendForgotEmail
from util.auth_services import checkAuthorization
from hashlib import sha256

@api.route('/register')
class Register(Resource):
    
    @api.doc(description='''
        Registers a user, sends an email to the specified student's university email
        with a token to activate that needs to be sent to `/api/auth/activate`
    ''')
    @api.expect(toModel(api, RegisterDetailsSchema))
    @validateBody(RegisterDetailsSchema, 'user')
    def post(self, user):
        if Users.query.filter_by(zID=user.zID).first():
            abort(403, {"zID": "Already registered user"})

        token = generateActivationToken(user)
        if sendActivationEmail(token, user.zID, user.firstName) != "success":
            abort(500, "Internal Server Error, Email Service Not Working")
        print(token)

        db.session.add(user)
        db.session.commit()
        #z5214808

        return jsonify({"status": "success", "data": {"token": token}})

@api.route('/login')
class Login(Resource):
    
    @api.doc(description='''
        Authorizes a user and returns a timestamped token
    ''')
    @api.expect(toModel(api, LoginDetailsSchema))
    @validateBody(LoginDetailsSchema, 'details')
    def post(self, details):
        if not details:
            abort(403, "Invalid Parametres, zID or password incorrect")

        token = generateLoginToken(details)

        return jsonify({"status": "success", "data": {"token": token}})

@api.route('/activate')
class Activate(Resource):

    @api.doc(description='''
        Takes token that was emailed to student when they registered using `/api/auth/register` 
        and now gives them 'activated' status from now on.      
    ''')
    #@api.expect(authModel)
    @checkAuthorization(activationRequired=False, level=0)
    def post(self, token_data):
        user = Users.query.filter_by(zID=token_data['zID']).first()
        if not user:
            abort(403, "Invalid Token, how did you know our server secret key?")

        user.activated = True
        db.session.add(user)
        db.session.commit()

        return jsonify({"status": "success"})

@api.route('/activate/resend')
class ReActivate(Resource):
    @api.doc(description='''
        Resend activation token to the account owner
    ''')
    @api.expect(toModel(api, ZIDSchema))
    @validateArgs(ZIDSchema, 'user')
    def post(self, user):
        if not user:
            abort(403, "Not a valid user")
        elif user.activated == True:
            abort(403, "Already activated")

        token = generateActivationToken(user)
        print(f"Token: {token}")
        if sendActivationEmail(token, user.zID, user.firstName) != "success":
            abort(500, "Internal Server Error, Email Service Not Working")

        return jsonify({"status": "success"})

@api.route('/forgot')
class Forgot(Resource):

    @api.doc(description='''
        Sends an email to the given zIDs student email with a temporary token that can be used in
        `/api/auth/reset` to reset the password
    ''')
    @api.expect(toModel(api, ZIDSchema))
    @validateArgs(ZIDSchema, 'user')
    def post(self, user):
        if not user:
            abort(400, "No such user")

        token = generateForgotToken(user.zID)
        print(f"Forgot Token: {token}")
        status = sendForgotEmail(token, user.zID)
        if status != "success":
            abort(500, "Internal Server Error, Email Service Not Working")

        return jsonify({"status": "success"})
        
@api.route('/reset')
class Reset(Resource):
    
    @api.doc(description='''
        Takes a token in the header that was generated in `/api/auth/forgot` and emailed
        to the student
        Expects new password in body
    ''')
    @api.expect(toModel(api, PasswordSchema), authModel)
    @checkAuthorization(level=0, activationRequired=False, type='forgot')
    @validateBody(PasswordSchema)
    def post(self, token_data, data):
        from hashlib import sha256
        user = Users.query.filter_by(zID=token_data['zID']).first()
        user.password = sha256(data['password'].encode()).hexdigest()

        db.session.add(user)
        db.session.commit()

        return jsonify({'status': 'success'})

@api.route('/change')
class changePassword(Resource):

    @api.doc(description='''
        Takes in a password for the user 
        TODO should probably also take old password
    ''')
    @api.expect(toModel(api, ChangePasswordSchema), authModel)
    @checkAuthorization(level=1)
    @validateBody(ChangePasswordSchema)
    def post(self, token_data, data):
        from hashlib import sha256
        user = Users.query.filter_by(zID=token_data['zID']).first()
        if (not sha256(data['oldPassword'].encode()).hexdigest() == user.password):
            abort(403, "Incorrect password")
            
        user.password = sha256(data['newPassword'].encode()).hexdigest()
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'status': 'success'})

@api.route('/validate')
@api.param('token', description='User Token', type='String', required='True')
class Authorize(Resource):

    @api.doc(description='''
        Status 200 if valid token
    ''')
    @api.expect(authModel)
    @checkAuthorization(level=1)
    def post(self, token_data):
        return jsonify({"valid" : "true"})



# Validation functions To be removed
@api.route('/validateSelf')
@api.param('token', description='User Token', type='String', required='True', location='headers')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    # @auth_services.check_authorization(activationRequired=False, level=5, allowSelf=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})

@api.route('/validateSocietyAdmin')
@api.param('token', description='User Token', type='String', required='True')
@api.param('societyID', description='Society ID', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    # @auth_services.check_authorization(level=5, allowSocStaff=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})
        
@api.route('/validateEventAdmin')
@api.param('token', description='User Token', type='String', required='True')
@api.param('eventID', description='Event ID', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    # @auth_services.check_authorization(level=5, allowSocStaff=True)
    def post(self, token_data):
        return jsonify({"valid" : "true"})
