import jwt
from datetime import datetime, date, time, timedelta
from util.users import checkUserInfo, checkUser, createUser
from flask_restx import abort

# Expiration time on tokens - 60 minutes
token_exp = 60*60
users = {}

def authorize_token(token):
    try:
        token_data = jwt.decode(
            token,
            'secret',
            algorithms='HS256'
        )
        return {"valid": True, "data": token_data}
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

def authorize(token):
    try:
        token_data = jwt.decode(
            token,
            'secret',
            algorithms='HS256'
        )
        return {"valid": True, "data": token_data}
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

def register_user(username, password):
    if (checkUser(username) == False):
        return True if createUser(username, password) == "Success" else False
    return False

def login(username, password):
    results = checkUserInfo(username, password)
    if (results == True):
        global token_exp
        token = jwt.encode(
            {
                'exp': datetime.utcnow() + timedelta(seconds=token_exp),
                'iat': datetime.utcnow(),
                'username': username
            }, 
            'secret', algorithm='HS256' # TODO ensure secret is secret
        ) 
        return token.decode("utf-8")
    return None