from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from util.auth_services import *
from marshmallow import Schema, fields, ValidationError, validates, validate
from util import utilFunctions

api = Namespace('other', description='Other utility routes')

@api.route("/onThisDay")
class onThisDay(Resource):
    def get(self):
        interval = request.args.get('interval')
        intervalType = request.args.get('intervalType')
        socID = request.args.get('socID')

        if (interval is None or intervalType is None):
            return dumps({"status": "Failed", "msg": "No date provided"})

        return dumps(utilFunctions.onThisDay(interval, intervalType)) if socID == None else dumps(utilFunctions.onThisDay(interval, intervalType, socID))
