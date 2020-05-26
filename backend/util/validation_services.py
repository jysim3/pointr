from flask import request, abort, jsonify
from flask_restx import fields
from marshmallow import ValidationError
from marshmallow.utils import missing

def validate_with(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):

            if not request.json:
                abort(400, 'Malformed Request')
            
            # Validate data
            try:
                data = schema().load(request.get_json())
            except ValidationError as err:
                abort(400, err.messages)
            return func(data=data, *args, **kwargs)
        return wrapper
    return decorator

def validateWith(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):

            if not request.json:
                abort(400, 'Request is not JSON')
            
            # Validate data
            try:
                data = schema().load(request.get_json())
            except ValidationError as err:
                abort(400, err.messages)
            return func(data=data, *args, **kwargs)
        return wrapper
    return decorator
    
def validate_args_with(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Validate data
            try:
                data = schema().load(request.args)
            except ValidationError as err:
                abort(400, err.messages)
            return func(args_data=data, *args, **kwargs)
        return wrapper
    return decorator

def validateArgsWith(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Validate data
            try:
                data = schema().load(request.args)
            except ValidationError as err:
                abort(400, err.messages)
            return func(argsData=data, *args, **kwargs)
        return wrapper
    return decorator

schemaNameToModel = {
    'String': fields.String,
    'Integer': fields.Integer,
    'DateTime': fields.DateTime,
    'AwareDateTime': fields.DateTime,
    'Boolean': fields.Boolean,
    'List': fields.List
}

def toModel(api, schema):

    modelFields = {}
    schemaFields = vars(schema)['_declared_fields']

    for schemaFieldName in schemaFields:
        # TODO add more documentation
        schemaField = schemaFields[schemaFieldName]

        modelFields[schemaFieldName] = schemaNameToModel[type(schemaField).__name__](
            required=schemaField.required,
            description=(schemaField.description if hasattr(schemaField,'description') else 'No description'),
            example=(schemaField.example if hasattr(schemaField,'example') else None),
        )

    return api.model(schema.name, modelFields)

def toQuery(api, schema):

    parser = api.parser()
    schemaFields = vars(schema)['_declared_fields']

    for schemaFieldName in schemaFields:
        # TODO add more documentation
        schemaField = schemaFields[schemaFieldName]
        
        parser.add_argument(schemaFieldName, 
            required=schemaField.required,
            help=(schemaField.description if hasattr(schemaField,'description') else None),
            default=(schemaField.default if not schemaField.default == missing else None),
        )

    return parser