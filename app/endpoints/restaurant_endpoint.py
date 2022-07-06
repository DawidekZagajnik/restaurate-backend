from flask import Blueprint, request
from app.db_models import Restaurant
from app.service.db import db
from app.domain.restaurant_payload import RestaurantPayload


restaurant_blueprint = Blueprint("restaurant_endpoints", __name__, template_folder=None)


@restaurant_blueprint.route("/restaurant", methods=["POST", "GET", "DELETE"])
def restaurant_endpoints(*args, **kwargs):
    if request.method == "GET":
        result = Restaurant.query.get(request.args["id"])
        if result is None:
            return f"Restaurant with ID {request.args['id']} does not exist", 404
        return result.dict()

    elif request.method == "POST":
        payload = RestaurantPayload(**request.json)
        result = Restaurant.query.filter_by(name=payload.name)
        if result is not None:
            return f"Restaurant with name {payload.name} already exists", 409

        restaurant = Restaurant(**payload.dict())
        db.session.add(restaurant)
        db.session.commit()

        return {"inserted": 1}

    # TODO MAKE IT ACCESSIBLE ONLY FOR OWNER
    elif request.method == "DELETE":
        result = Restaurant.query.get(request.args["id"])
        if result is None:
            return f"Restaurant with ID {request.args['id']} does not exist", 404

        db.session.delete(result)
        db.session.commit()
        return "Deleted", 200
