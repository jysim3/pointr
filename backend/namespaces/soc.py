from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, reqparse
from util.sanitisation_services import sanitize
from util import societies, utilFunctions

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

@api.route('/makeStaff')
class MakeStaff(Resource):
    def post(self):
        data = request.get_json()
        if ('zID' not in data or 'socID' not in data):
            abort(400, "Malformed Request")
        # TODO: Complete This
