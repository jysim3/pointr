from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from util.auth_services import *
from marshmallow import Schema, fields, ValidationError, validates, validate
from util import societies
from flask import jsonify

api = Namespace('soc', description='societies-related routes')

@api.route('/getAllSocs')
class getSocs(Resource):
    def get(self):
        return jsonify(societies.getAllSocs())

@api.route('/joinSoc')
class joinSoc(Resource):
    def post(self):
        data = request.get_json()
        if ('zID' not in data or 'socID' not in data):
            abort(400, "Malformed Request")
        result = societies.joinSoc(str(data['zID']), str(data['socID']))
        if result == 'failed':
            abort(400, "Bad arguments")
        return jsonify({"status": "success"})

@api.route('/makeStaff')
class makeStaff(Resource):
    def post(self):
        data = request.get_json()
        if ('zID' not in data or 'socID' not in data):
            abort(400, "Malformed Request")
        # TODO: Complete This