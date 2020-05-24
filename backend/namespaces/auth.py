from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, reqparse
from util import auth_services, users, utilFunctions, societies
from util.auth_services import ADMIN, USER
from schemata.auth_schemata import RegisterDetailsSchema, LoginDetailsSchema, TokenSchema, ZIDDetailsSchema, PasswordSchema
from marshmallow import Schema, fields, ValidationError, validates, validate
from util.validation_services import validate_with, validate_args_with
import pprint
import uuid

# SQLAlchemy
from app import db
from models.user import Users
from hashlib import sha256
#from smtplib import SMTPConnectError, SMTPServerDisconnected

api = Namespace('auth', description='Authentication & Authorization Services')

@api.route('/register')
class Register(Resource):
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @api.response(409, 'Username Taken')
    @validate_with(RegisterDetailsSchema)
    # NOTE: As of 20/05/2020, data is now a object of type Users
    # We can load this directly into the db
    def post(self, data):
        from util.emailPointr import sendActivationEmail
        # Step 1, check for validity of the zID
        if Users.query.filter_by(zid=data.zid).first():
            abort(409, "username taken")

        # Step 2, try sending an email, if error occurs, abort
        token = auth_services.generateActivationToken(data.zid)
        results = sendActivationEmail(f"/activate/{token}", f"{data.zid}@student.unsw.edu.au")
        if (results != "success"):
            # This only happens if we have some kind of SMTP error, most likely due to security measures on unrecognised devices
            abort(400, "Sending Email Not Successful")

        # Step 3, inject the user into the database
        db.session.add(data)
        db.session.commit()

        return jsonify({"status": "success"})

@api.route('/login')
class Login(Resource):
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @validate_with(LoginDetailsSchema)
    def post(self, data):
        user = Users.query.filter_by(zid=data['zID'], 
            password=sha256(data['password'].encode('UTF-8')).hexdigest()).first()

        if not user: abort(403, 'Invalid Credentials / Account Not Activated')

        token = auth_services.generateLoginToken(user)
        return jsonify({"token": token})

# NOTE: DEFUNCT
@api.route('/activate')
class Activate(Resource):
    @api.header('Authorization', description='Activation token sent to email after call to /api/auth/register', type='String', required=True)
    @api.response(400, "Malformed Request")
    @api.response(403, "Already activated")
    @api.doc(responses={})
    @auth_services.check_authorization(activationRequired=False, level=0)
    def post(self, token_data):

        result = users.activateAccount(token_data['zID'].lower())
        if (result == "failed"):
            abort(400, "Malformed Request")
        elif (result == "already activated"):
            abort(403, "Already activated")
        return jsonify({"status": "success"})

@api.route('/forgot')
class Forgot(Resource):
    
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @validate_with(ZIDDetailsSchema)
    def post(self, data):
        
        # Login and if successful return the token otherwise invalid credentials
        token = auth_services.generateForgotToken(data['zID'])
        
        from util.emailPointr import sendForgotEmail
        results = sendForgotEmail(f"/resetPassword/{token}", data['zID'], f"{data['zID']}@student.unsw.edu.au")  
        if (results != "success"):
            abort(400, "Sending Email Not Successful")
        return jsonify({"msg": "success"})
        
@api.route('/reset')
class Reset(Resource):
    
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @auth_services.check_authorization(level=0, activationRequired=False)
    @validate_with(PasswordSchema)
    @api.doc(description="When given a password in body and a token created through /api/auth/forgot and retrived through emails in the Authorization header, this endpoint will update the password of the token's owner")
    def post(self, token_data, data):
        # TODO make check_authorization also take in type
        if (not token_data['type'] == 'forgot'):
            abort('403', 'Invalid Credentials')
        if (users.changePassword(token_data['zID'], data['password']) == 'failed'):
            abort('400', "Invalid")
        return jsonify({"status": "success"})

@api.route('/changePassword')
class changePassword(Resource):
    @auth_services.check_authorization(level = 1)
    def post(self, token_data):
        data = request.get_json()
        if 'password' not in data or 'oldPassword' not in data:
            abort(400, "No password provided")
        if (users.changePassword(token_data['zID'], data['oldPassword'], data['password']) == 'failed'):
            abort(400, "Server Error, check backend log")
        return jsonify({"status": "success"})

@api.route('/permission')
class Permission(Resource):
    
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @auth_services.check_authorization(activationRequired=False, level=0)
    def post(self, token_data):
        return jsonify({"permission": token_data['permission']})

@api.route('/validate')
@api.param('token', description='User Token', type='String', required='True')
class Authorize(Resource):

    @api.response(400, 'Malformed Request')
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        return jsonify({"valid" : "true"})

# Validation functions
@api.route('/validateSelf')
@api.param('token', description='User Token', type='String', required='True')
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
