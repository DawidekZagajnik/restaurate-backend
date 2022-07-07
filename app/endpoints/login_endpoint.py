from flask import Blueprint, request
from app.db_models import User
from hashlib import sha1
from app.utils.auth.auth_middleware import set_token


login_blueprint = Blueprint("login_endpoint", __name__, template_folder=None)


@login_blueprint.route("/login", methods=["POST"])
def login_user():
    user = User.query.filter_by(username=request.json["username"]).first()
    if user:
        password = request.json["password"]
        if user.passHash == sha1(f"{user.salt}{password}".encode("utf-8")).hexdigest():
            return set_token(user), 200

        else:
            return "Username or password are incorrect", 401
    else:
        return "Username or password are incorrect", 401
