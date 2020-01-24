import jwt
from datetime import datetime, date, time, timedelta

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
        return {"valid": False, "reason": "Invalid token signature"}
    except jwt.ExpiredSignatureError:
        print("Received expired token")
        return {"valid": False, "reason": "Expired token"}
    return {"valid": False, "reason": "Unknown"}

def register_user(username, password):
    global users
    if (not users.get(username)):
        users[username] = password
        return True
    return False

def login(username, password):
    global users
    if (users.get(username) == password):
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
    return False