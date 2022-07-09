from flask import Blueprint, request
from app.db_models import User
from app.service.db import db
from app.domain.user_payload import UserPayload
from hashlib import sha1
import random
from app.utils.auth.auth_middleware import requires_auth
from pydantic import ValidationError

user_blueprint = Blueprint("user_endpoints", __name__, template_folder=None)


@user_blueprint.route("/user/<id>", methods=["GET", "DELETE"])
@requires_auth()
def user_endpoints(curr_user: User, id: int):
    if curr_user.id != id:
        return f"You can delete only your account.", 409

    user = User.query.get(id)
    if not user:
        return f"User with ID {id} not found.", 404

    db.session.delete(user)
    db.session.commit()
    return {"deleted": 1}


@user_blueprint.route("/user/<id>", methods=["GET"])
@requires_auth(return_user=False)
def get_user(id: int):
    user = User.query.get(id)
    if user:
        return user.dict()
    else:
        return f"User with ID {id} not found.", 404


@user_blueprint.route("/my-account", methods=["GET"])
@requires_auth()
def my_account_endpoint(curr_user: User):
    user = User.query.get(curr_user.id)
    if user:
        return user.dict()
    else:
        return f"User with ID {id} not found.", 404


@user_blueprint.route("/user", methods=["POST"])
def register_user():
    try:
        payload = UserPayload(**request.json)

    except ValidationError as e:
        return str(e), 422

    result = User.query.filter_by(username=payload.username).first()
    if result:
        return f"User with username {payload.username} already exists.", 409

    salt = ''.join(chr(random.randint(32, 126)) for _ in range(20))
    password_hash = sha1(f"{salt}{payload.password}".encode('utf-8')).hexdigest()

    user = User(username=payload.username, passHash=password_hash, salt=salt)
    db.session.add(user)
    db.session.commit()

    return {"inserted": 1}
