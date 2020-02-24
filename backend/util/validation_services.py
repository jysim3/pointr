from flask import request, abort, jsonify
from marshmallow import ValidationError

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