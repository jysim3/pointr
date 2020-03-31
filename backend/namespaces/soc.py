from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, reqparse
from util.sanitisation_services import sanitize
from util import societies, utilFunctions, auth_services, events
from util.validation_services import validate_args_with, validate_with
from util.files import uploadImages
from schemata.soc_schemata import SocietyIDAndZIDSchema, SocietyIDSchema
import pprint
from json import loads

api = Namespace('soc', description='Society Attendance Services')

# Get all the events hosted by a society
@api.param('token', description='User Token', type='String', required='True')
@api.route('')
class Society(Resource):
    @api.doc(description='''
        Get all of the events hosted by a society
    ''')
    @auth_services.check_authorization(level=1)
    @api.param('societyID', description='ID of the queried society', type='String', required='True')
    def get(self, token_data):
        societyID = request.args.get("societyID")
        if societyID == None: abort(400, "Malformed Request")
                
        eventsList = societies.getEventForSoc(societyID)
        
        if (eventsList == "No such society"):
            return jsonify({"status": "Failed", "msg": "No such society"})

        return jsonify(eventsList)

    @api.doc(description='''
        Create a new society
    ''')
    # FIXME: USING LEVEL 1 TOKENS TO TEST FUNCTIONALITIES, CHANGE THIS BACK TO 2 IN PRODUCTION
    @auth_services.check_authorization(level=1)
    def post(self, token_data):
        data = request.form['json']
        data = loads(data)

        # TODO: If we make a decision on using images, add sql query down below
        # For image upload
        file = None
        if request.files:
            file = request.files['file']

        if (data is None or 'societyName' not in data):
            abort(400, "SocietyName not given in request")

        # TODO: Chuck files to the end of this function
        result = societies.createSociety(token_data['zID'], sanitize(data['societyName']), False, file)
        if (result == "exists already"):
            abort(403, "A society with this name already exists")
        elif (isinstance(result, tuple) != True):
            print(result)
            abort(400, "A server error occurred (most likely a database fault), check backend log for more details")
        return jsonify({"msg": result[0]})
        
# Making an account by admin (required Superadmin)
@api.param('token', description='User Token', type='String', required='True')
@api.route('/makeAdmin')
class Society(Resource):
    @api.doc(description='''
        Allows an superadmin (i.e. acounts with clearance level >= 2)
    ''')
    @auth_services.check_authorization(level=1)
    #@validate_args_with(SocietyIDAndZIDSchema)
    @api.param('societyID', description='ID of the queried society', type='String', required='True')
    @api.param('zID', description='ID of the target account', type='String', required='True')

    def post(self, token_data):
        authorzID = token_data['zID']
        parametres = request.get_json()
        zID = parametres['zID'] if 'zID' in parametres else abort (400, "Malformed Request")
        societyID = parametres['societyID'] if 'societyID' in parametres else abort (400, "Malformed Request")
        # First check if the token zid is an admin of the soc
        isAdmin = societies.checkAdmin(societyID, authorzID)
        if isAdmin == False:
            abort(405, "Not an admin for this particular society, unable to process request")
        result = societies.makeAdmin(zID, societyID)

        if (result == "failed"):
            abort(403, "zID/societyID not valid")
        return jsonify({"status": "success"})

@api.param('token', description='User Token', type='String', required='True')
@api.route('/getAllSocs')
class GetSocs(Resource):
    @auth_services.check_authorization(level=1)
    def get(self, token_data):
        return jsonify(societies.getAllSocs())

@api.param('token', description='User Token', type='String', required='True')
@api.route('/join')
class Join(Resource):
    @auth_services.check_authorization(level=1)
    @validate_with(SocietyIDSchema)
    def post(self, token_data, data):

        result = societies.joinSoc(token_data['zID'], data['societyID'])
        if result == 'failed':
            abort(400, "Bad arguments")
        elif result == "Already registered":
            abort(403, "Already a part of the society")
        return jsonify({"status": "success"})

    def delete(self):
        #TODO
        pass
        
#Example society BCEB9

@api.route('/staff')
class Staff(Resource):
    
    @api.doc(description='''
        Make a zID a staff member of this society
    ''')
    #FIXME change back auth level
    
    @auth_services.check_authorization(level=1, allowSocStaff=True)
    @api.param('societyID', description='SocietyID of Society of interest', type='String', required='True')
    @api.param('zID', description='zID of Person to become admin of society', type='String', required='True')
    @api.param('token', description='User Token', type='String', required='True')
    @validate_args_with(SocietyIDAndZIDSchema)
    def post(self, token_data, args_data):
        return societies.makeAdmin(args_data['zID'], args_data['societyID'])
    
    @api.doc(description='''
        Get all staff members of this society
    ''')
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    @api.param('societyID', description='SocietyID of Society to get admins of', type='String', required='True')
    @validate_args_with(SocietyIDSchema)
    def get(self, token_data, args_data):
        status = societies.getAdminsForSoc(args_data['societyID'])
        return jsonify(status)
    
    @api.doc(description='''
        Remove staff member
    ''')
    @auth_services.check_authorization(level=2, allowSocStaff=True)
    def delete(self):
        #TODO
        pass

@api.route("/getPastEvents")
class getPast(Resource):
    def get(self):
        socID = request.args.get('socID')
        if socID == None:
            abort(400, "Can't find socID")
        results = events.getPastEvents(socID)
        return jsonify(results)

@api.route("/getSocLogo")
class getLogo(Resource):
    #@auth_services.check_authorization(level=1)
    def get(self):
        socID = request.args.get('socID')
        if socID == None:
            abort(400, "Can't find socID") 
        results = societies.getSocLogo(socID)
        if (results == None):
            return jsonify({"msg": results})
        elif (isinstance(results, tuple) == False):
            abort(400, results)
        return jsonify({"msg": results[0]})