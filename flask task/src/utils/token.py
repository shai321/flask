from jose import jwt
from datetime import datetime, timedelta
from src.config import Config
import jwt as jwt_error
from flask import request, g
from flask_api import status
from functools import wraps
from src.utils.error_handel import TaskException

def create_access_token(subject: dict, expire_time=timedelta(days=1)):
    if expire_time:
        expire_time = datetime.utcnow() + expire_time
    data = {**subject, "exp": expire_time}
    return jwt.encode(data, key=Config.JWT_SECRET_KEY, algorithm="HS256")


def token_required(s):
    @wraps(s)
    def check_token(*args, **kwargs):
        try:
            bearer_token = request.headers.get('Authorization')
            token = bearer_token.split()[1]
            decode_token = jwt.decode(
                token=token, key=Config.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            user = type("MyObject", (object,), decode_token)
            g.user_data = user
            if decode_token["exp"] >= datetime.timestamp(datetime.now()):
                return s(*args, **kwargs)
            else:
                raise TaskException(
                    message="token is expired", status_code=status.HTTP_401_UNAUTHORIZED
                )
        except jwt_error.exceptions.InvalidTokenError:
            raise TaskException(
                message="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED
            )

    return check_token
    
   
