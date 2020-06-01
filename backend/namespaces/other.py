from flask import abort, jsonify
from flask_restx import Namespace, Resource

api = Namespace("other", description="General routes")

from util.emailPointr import sendEnquiry
from util.validation_services import validateBody, toModel
from util.auth_services import checkAuthorization
from schemata.common_schemata import MessageSchema
from schemata.models import authModel
from models.user import Users

@api.route("/enquire")
class Enquire(Resource):
    @api.doc('''
        Use this route for the users to send any enqueries or file bug reports
    ''')
    @api.expect(authModel, toModel(api, MessageSchema))
    @validateBody(MessageSchema, 'message')
    @checkAuthorization(level=1)
    def post(self, token_data, message):
        status = sendEnquiry(token_data['zID'], message['message'])

        if status != "success":
            abort(500, "Something's up with our server, please try again later")

        return jsonify({'status': 'success'})