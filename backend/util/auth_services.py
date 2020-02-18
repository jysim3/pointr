import jwt
from datetime import datetime, date, time, timedelta
from util.users import checkUserInfo, checkUser, createUser
from flask_restx import abort

# Expiration time on tokens - 60 minutes
token_exp = 60*60
users = {}
ADMIN = 'Admin'
USER = 'User'

def authorize_token(token, permission):
    try:
        token_data = jwt.decode(
            token,
            'secret',
            algorithms='HS256'
        )
        global ADMIN, USER
        if (permission == token_data['permission']):
            return {"valid": True, "data": token_data}
        elif (token_data['permission'] == ADMIN and permission == USER):
            return {"valid": True, "data": token_data}
        else:
            return {"valid": False, "reason": "Permission denied"}
    except jwt.InvalidSignatureError:
        print("Received invalid token signature")
        return {"valid": False, "reason": "Invalid token"}
    except jwt.ExpiredSignatureError:
        print("Received expired token")
        return {"valid": False, "reason": "Expired token"}
    except jwt.DecodeError:
        print("Received invalid token data")
        return {"valid": False, "reason": "Invalid token"}
    return {"valid": False, "reason": "Unknown"}

def authorize(token, permission):
    try:
        token_data = jwt.decode(
            token,
            'secret',
            algorithms='HS256'
        )
        global ADMIN, USER
        if (permission == token_data['permission']):
            return {"valid": True, "data": token_data}
        elif (token_data['permission'] == ADMIN and permission == USER):
            return {"valid": True, "data": token_data}
        else:
            abort(401, "Permission Denied")
    except jwt.InvalidSignatureError:
        print("Received invalid token signature")
        abort(403, 'Invalid Credentials')
    except jwt.ExpiredSignatureError:
        print("Received expired token")
        abort(401, 'Expired Token')
    except jwt.DecodeError:
        print("Received invalid token data")
        abort(403, 'Invalid Credentials')
    abort(400, 'Malformed Request')

def register_user(zID, password):
    if (checkUser(zID) == False):
        return True if createUser(zID, password) == "Success" else False
    return False

def login(zID, password):
    results = checkUserInfo(zID, password)
    if (results == True):
        global token_exp
        token = jwt.encode(
            {
                'exp': datetime.utcnow() + timedelta(seconds=token_exp),
                'iat': datetime.utcnow(),
                'zID': zID,
                'permission': USER # TODO Make it so admins and users can be created
            }, 
            'secret', algorithm='HS256' # TODO ensure secret is secret
        ) 
        return token.decode("utf-8")
    return None