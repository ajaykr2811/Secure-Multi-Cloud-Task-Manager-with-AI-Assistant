import time
import jwt
from functools import wraps
from flask import request, current_app
import config

#generate a signed JWT token
def generate_token(payload: dict, exp_seconds: int | None = None) -> str:
    exp = int(time.time()) + (exp_seconds or config.JWT_EXPIRATION_SECONDS)
    to_encode = {**payload, "exp": exp, "iat": int(time.time())}
    token = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALG)
    return token

def decode_token(token:str) -> dict:
    return jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALG])

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return {"message": "Missing or invalid Authorization header"}, 401
        token = auth.split(" ", 1)[1].strip()
        try:
            claims = decode_token(token)
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401
        #pass claims to the route function
        return fn(claims, *args, **kwargs)
    return wrapper