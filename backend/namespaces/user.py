from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from flask_restx import fields as flask_fields
from json import dumps
from utils.auth_services import *
from models.models import *
from marshmallow import Schema, fields, ValidationError, validates, validate

api = Namespace('user', description='User Services')