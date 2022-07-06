from flask import Blueprint, request
from app.db_models import User
from app.service.db import db
from app.domain.user_payload import UserPayload
from hashlib import sha1
import random


user_blueprint = Blueprint("user_endpoints", __name__, template_folder=None)


@user_blueprint.route("/user", methods=["POST", "GET", "DELETE"])
def hello():
    if request.method == "POST":
        payload = UserPayload(**request.json)
        result = User.query.filter_by(username=payload.username)
        if result is not None:
            return f"User with username {payload.username} already exists", 409

        salt = ''.join(chr(random.randint(32, 126)) for _ in range(20))
        password_hash = sha1(f"{salt}{payload.password}".encode('utf-8')).hexdigest()

        user = User(username=payload.username, passHash=password_hash, salt=salt)
        db.session.add(user)
        db.session.commit()

        return {"inserted": 1}

    elif request.method == "GET":
        result = User.query.get(request.args["id"])
        if result:
            return result
        else:
            return f"No user with ID {request.args['id']} found", 404

    elif request.method == "DELETE":
        result = User.query.get(request.args["id"])
        if result:
            db.session.delete(result)
            db.session.commit()
            return "Deleted", 200
        else:
            return f"User with ID {request.args['id']} not found", 404

