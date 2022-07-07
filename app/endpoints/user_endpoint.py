from flask import Blueprint, request
from app.db_models import User
from app.service.db import db
from app.domain.user_payload import UserPayload
from hashlib import sha1
import random
from app.utils.auth.auth_middleware import requires_auth


user_blueprint = Blueprint("user_endpoints", __name__, template_folder=None)


@user_blueprint.route("/user", methods=["GET", "DELETE"])
@requires_auth()
def user_endpoints(curr_user: User):

    return ""


@user_blueprint.route("/user", methods=["POST"])
def register_user():
    payload = UserPayload(**request.json)
    result = User.query.filter_by(username=payload.username).first()
    if result:
        return f"User with username {payload.username} already exists", 409

    salt = ''.join(chr(random.randint(32, 126)) for _ in range(20))
    password_hash = sha1(f"{salt}{payload.password}".encode('utf-8')).hexdigest()

    user = User(username=payload.username, passHash=password_hash, salt=salt)
    db.session.add(user)
    db.session.commit()

    return {"inserted": 1}
