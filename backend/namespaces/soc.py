from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, reqparse
from util.sanitisation_services import sanitize
from util import societies, utilFunctions, auth_services
from util.validation_services import validate_args_with, validate_with
from schemata.soc_schemata import SocietyIDAndZIDSchema, SocietyIDSchema
import pprint

api = Namespace('soc', description='Society Attendance Services')

# Get all the events hosted by a society
@api.route('/')
class Society(Resource):
    @api.doc(description='''
        Get all of the events hosted by a society
    ''')
    @api.param('societyID', description='ID of the queried society', type='String', required='True')
    def get(self):
        societyID = request.args.get('societyID')
        if (societyID is None):
            return jsonify({"status": "Failed", "msg": "No societyID inputted"})
        eventsList = societies.getEventForSoc(societyID)
        if (eventsList == "No such society"):
            return jsonify({"status": "Failed", "msg": "No such society"})
        
        payload = {}
        payload['events'] = []
        payload['societyName'] = eventsList[1]
        for event in eventsList[0]:
            eventJSON = {}
            eventJSON['eventID'] = event[0]
            eventJSON['name'] = event[1]
            eventJSON['society'] = event[3]
            eventJSON['eventDate'] = str(event[2])
            payload['events'].append(eventJSON)
        return jsonify(payload)
    
    @api.doc(description='''
        Create a new society
    ''')
    def post(self):
        data = request.get_json()
        
        result = societies.createSociety(sanitize(data['founder'] if data['founder'] is not None else 'Not Applicable'), sanitize(data['societyName']))
        if (result == "exists already"):
            return jsonify({"status": "Failed", "msg": "A society with this name already exists"})
        return jsonify({"status": "Success", "msg": result})
        
@api.route('/getAllSocs')
class GetSocs(Resource):
    def get(self):
        return jsonify(societies.getAllSocs())

@api.route('/join')
class Join(Resource):
    def post(self):
        data = request.get_json()
        if ('zID' not in data or 'socID' not in data):
            abort(400, "Malformed Request")
        result = societies.joinSoc(str(data['zID']), str(data['socID']))
        if result == 'failed':
            abort(400, "Bad arguments")
        return jsonify({"status": "success"})
        
#Example society BCEB9

@api.route('/staff')
class Staff(Resource):
    
    @api.doc(description='''
        Make a zID a staff member of this society
    ''')
    #FIXME change back auth level
    @auth_services.check_authorization(level=1, allowSocStaff=True)
    @validate_args_with(SocietyIDAndZIDSchema)
    def post(self, token_data, args_data):
        return societies.makeAdmin(args_data['zID'], args_data['societyID'])
    
    @api.doc(description='''
        Get all staff members of this society
    ''')
    @auth_services.check_authorization(level=2, allowSocStaff=True)
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
