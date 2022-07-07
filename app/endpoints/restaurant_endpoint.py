from flask import Blueprint, request
from app.db_models import Restaurant
from app.service.db import db
from app.domain.restaurant_payload import RestaurantPayload


restaurant_blueprint = Blueprint("restaurant_endpoints", __name__, template_folder=None)


@restaurant_blueprint.route("/restaurant", methods=["POST", "GET", "DELETE"])
def restaurant_endpoints():
    return ""
