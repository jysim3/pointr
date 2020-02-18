from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from util.auth_services import *
from marshmallow import Schema, fields, ValidationError, validates, validate
from util import societies

api = Namespace('soc', description='societies-related routes')

@api.route('/getAllSocs')
class getSocs(Resource):
    def get(self):
        return dumps(societies.getAllSocs())