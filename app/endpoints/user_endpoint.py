from flask import Blueprint

user_blueprint = Blueprint("user_endpoints", __name__, template_folder=None)


@user_blueprint.route("/")
def hello():
    return {"hello": True}
