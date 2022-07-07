from flask import request
from functools import wraps
from app.service.redis_client import redis_client
from app.db_models import User
from secrets import token_hex


def requires_auth():

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _, token = request.headers.get("Authorization", "Bearer ").split(" ")
            user = redis_client.client.get(f"AUTH-{token}")

            if user is None:
                return "User not authenticated", 401

            redis_client.client.expire(name=f"AUTH-{token}", time=15 * 60)

            return func(User(**user), *args, **kwargs)

        return wrapper

    return decorator


def set_token(user: User):
    token = token_hex(20)

    redis_client.client.set(name=f"AUTH-{token}", value=user.dict(), ex=15 * 60)

    return token