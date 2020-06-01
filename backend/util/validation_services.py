from flask import request, abort, jsonify
from flask_restx import fields
from marshmallow import ValidationError
from marshmallow.utils import missing
from json import loads, dumps

def validateArgs(schema, name='argsData'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Validate data
            try:
                data = schema().load(request.args)
            except ValidationError as err:
                abort(400, err.messages)
           
            validatedData = {
                name: data
            }

            kwargs.update(validatedData)

            return func(*args, **kwargs)
        return wrapper
    return decorator

def validateBody(schema, name='data'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Validate data
            try:
                data = schema().load(request.get_json())
            except ValidationError as err:
                abort(400, err.messages)
           
            validatedData = {
                name: data
            }

            kwargs.update(validatedData)

            return func(*args, **kwargs)
        return wrapper
    return decorator

def validateForm(schema, name="formData"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not request.form:
                abort(400, "Missing Parametres")

            try:
                formData = schema().load(loads(dumps(dict(request.form))))
            except ValidationError as error:
                abort(400, error.messages)

            validatedData = {
                name: formData
            }

            kwargs.update(validatedData)

            return func(*args, **kwargs)
        return wrapper
    return decorator

schemaNameToModel = {
    'String': fields.String,
    'Integer': fields.Integer,
    'DateTime': fields.DateTime,
    'AwareDateTime': fields.DateTime,
    'Boolean': fields.Boolean,
    'List': fields.List,
    'UUID': fields.String
}

def toModel(api, schema):

    modelFields = {}
    schemaFields = vars(schema)['_declared_fields']

    for schemaFieldName in schemaFields:
        # TODO add more documentation
        schemaField = schemaFields[schemaFieldName]

        if type(schemaField).__name__ == 'List':
            innerField = schemaNameToModel[type(schemaFields[schemaFieldName].inner).__name__]
            
            modelFields[schemaFieldName] = schemaNameToModel[type(schemaField).__name__]( innerField,
                required=schemaField.required,
                description=(schemaField.description if hasattr(schemaField,'description') else 'No description'),
                example=(schemaField.example if hasattr(schemaField,'example') else None),
            )
        else:
            modelFields[schemaFieldName] = schemaNameToModel[type(schemaField).__name__](
                required=schemaField.required,
                description=(schemaField.description if hasattr(schemaField,'description') else 'No description'),
                example=(schemaField.example if hasattr(schemaField,'example') else None),
            )

    return api.model(schema.__schema_name__, modelFields)

def toQuery(api, schema):

    parser = api.parser()
    schemaFields = vars(schema)['_declared_fields']

    for schemaFieldName in schemaFields:
        # TODO add more documentation
        schemaField = schemaFields[schemaFieldName]

        parser.add_argument(schemaFieldName, 
            required=schemaField.required,
            type=type(schemaField).__name__,
            help=(schemaField.description if hasattr(schemaField,'description') else None),
            default=(schemaField.default if not schemaField.default == missing else None),
        )

    return parser