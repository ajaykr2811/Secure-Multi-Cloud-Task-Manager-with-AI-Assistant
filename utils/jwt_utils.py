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

