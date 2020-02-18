from flask import request, jsonify
from flask_restx import Namespace, Resource, abort, reqparse
from marshmallow import Schema, fields, ValidationError, validates, validate
from util import utilFunctions

api = Namespace('other', description='Other utility routes')

# Will probably be involved in some kind of a "today's events" type of thing
# Accepts three arguments (two compulsory)
# interval accepts either a date in the form of "YYYY-MM-DD", or a week in the form of "T[1-3]W[1-10]", or a month in the range of [1-12]
# intervalType accepts ['day', 'week', 'month']

# GET /api/events/onthisday?interval=2020-04-04&intervalType=day&socID=1AEF0 (Note: socID optional)
# Returns:
# [{"eventID": "1239", "name": "Test Event 0", "society": "UNSW Hall", "eventDate": "2019-11-19"}, {"eventID": "1240", "name": "Coffee Night", "society": "UNSW Hall", "eventDate": "2019-11-20"}]
@api.route("/onThisDay")
class onThisDay(Resource):
    def get(self):
        interval = request.args.get('interval')
        intervalType = request.args.get('intervalType')
        socID = request.args.get('socID')

        if (interval is None or intervalType is None):
            return jsonify({"status": "Failed", "msg": "No date provided"})

        return jsonify(utilFunctions.onThisDay(interval, intervalType)) if socID == None else jsonify(utilFunctions.onThisDay(interval, intervalType, socID))