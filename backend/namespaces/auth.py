from flask import request, jsonify, request
from flask_restx import Namespace, Resource, abort, reqparse
from util import auth_services, users, utilFunctions, societies
from util.auth_services import ADMIN, USER
from schemata.auth_schemata import RegisterDetailsSchema, LoginDetailsSchema, TokenSchema, ZIDDetailsSchema, PasswordSchema
from marshmallow import Schema, fields, ValidationError, validates, validate
from emailPointr import sendActivationEmail, sendForgotEmail
from util.validation_services import validate_with, validate_args_with
import pprint
import uuid
from smtplib import SMTPConnectError, SMTPServerDisconnected

# FIXME: Delete this after the first time we need to sign users on
import csv
zIDList = []
with open('zIDList.txt') as hallList:
    csv_reader = csv.reader(hallList, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        zIDList.append(row[0])
print("this was called")

api = Namespace('auth', description='Authentication & Authorization Services')

@api.route('/register')
class Register(Resource):
    # @api.response(200, 'Success', token_details)
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @api.response(409, 'Username Taken')
    @validate_with(RegisterDetailsSchema)
    def post(self, data):

        # Attempt to create a new user with the username and password
        zID = data['zID'].lower()
        password = data['password']
        firstName = data['firstName'] if 'firstName' in data else "John"
        lastName = data['lastName'] if 'lastName' in data else "Doe"
        isArc = data['isArc'] if 'isArc' in data else True
        commencementYear = data['commencementYear'] if 'commencementYear' in data else 2020
        studentType = data['studentType'] if 'studentType' in data else "domestic"
        degreeType = data['degreeType'] if 'degreeType' in data else "undergraduate"
        #floorGroup = data['floorGroup'] if 'floorGroup' in data else "unspecified"

        # Step 1, check for validity of the zID
        if (utilFunctions.checkUser(zID) == True):
            abort(409, "username taken") 

        # Step 2, try sending an email, if error occurs, abort
        try:
            token = auth_services.generateActivationToken(zID)
            sendActivationEmail(f"https://pointr.live/activate/{token}", f"{zID}@student.unsw.edu.au")
        except SMTPServerDisconnected as e:
            abort(400, "Sending email not successful")
        except SMTPConnectError as e:
            abort(400, "Email failed")

        # Step 3, inject the user into the database
        results = users.createUser(zID, firstName, lastName, password, isArc, int(commencementYear), studentType, degreeType)
        if results != "success":
            abort(403, results)

        # FIXME: PLEASE REMOVE ME AFTER THE FIRST TIME WE HAVE TO SIGN THE USERS ON
        global zIDList
        if (zID in zIDList):
            socID = societies.findSocID("UNSW Hall")
            results = societies.joinSoc(zID, socID)
            resultsForJoin = None
            isCol = societies.isCollege(socID)
            if (isCol == True):
                # TODO: Check for floorgroups of the zID
                resultsForJoin = None
                resultsForJoin = societies.joinCollege(zID, socID) # TODO: Doesn't work right now, add in floorgroup check
            if results != "success" or resultsForJoin != "success":
                return jsonify({"status": "kind of success", "msg": "Account created but could not join UNSW Hall"})

        return jsonify({"status": "success"})

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

@api.route('/login')
class Login(Resource):
    
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @validate_with(LoginDetailsSchema)
    def post(self, data):
        
        # Login and if successful return the token otherwise invalid credentials
        token = auth_services.login(data['zID'].lower(), data['password'])
        if (token):
            return jsonify({"token": token})
        else:
            abort(403, 'Invalid Credentials / Account Not Activated')

@api.route('/forgot')
class Forgot(Resource):
    
    @api.response(400, 'Malformed Request')
    @api.response(403, 'Invalid Credentials')
    @validate_with(ZIDDetailsSchema)
    def post(self, data):
        
        # Login and if successful return the token otherwise invalid credentials
        token = auth_services.generateForgotToken(data['zID'])
        
        sendForgotEmail(f"https://pointer.live/reset/{token}", data['zID'], f"{data['zID']}@student.unsw.edu.au")  
        
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
    @auth_services.check_authorization(activationRequired=False, level=0)
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
