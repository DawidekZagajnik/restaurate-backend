from flask import Blueprint, request
from app.db_models import Restaurant, User
from app.service.db import db
from app.domain.restaurant_payload import RestaurantPayload
from app.utils.auth.auth_middleware import requires_auth
from pydantic import ValidationError


restaurant_blueprint = Blueprint("restaurant_endpoints", __name__, template_folder=None)


@restaurant_blueprint.route("/restaurant/<id>", methods=["GET", "DELETE"])
@requires_auth()
def restaurant_endpoints(curr_user: User, id: int):
    if request.method == "GET":
        result = Restaurant.query.get(id)
        if not result:
            return f"Restaurant with ID {id} not found.", 404
        return result.dict()

    elif request.method == "DELETE":
        result = Restaurant.query.get(id)
        if not result:
            return f"Restaurant with ID {id} not found.", 404

        if curr_user.id != result.ownerId:
            return f"You can delete only your restaurant.", 409

        db.session.delete(result)
        db.session.commit()

        return {"deleted": 1}


@restaurant_blueprint.route("/restaurant", methods=["POST"])
@requires_auth()
def create_restaurant(curr_user: User):
    try:
        payload = RestaurantPayload(**request.json)

    except ValidationError as e:
        return str(e), 422

    result = Restaurant.query.filter_by(name=payload.name).all()
    if result:
        return f"Restaurant with name {payload.name} already exists.", 409

    restaurant = Restaurant(
        name=payload.name,
        description=payload.description,
        ownerId=curr_user.id
    )
    db.session.add(restaurant)
    db.session.commit()
    return {"inserted": 1}


@restaurant_blueprint.route("/restaurants", methods=["GET"])
@requires_auth()
def load_restaurants(_: User):
    start = request.args.get("start", 0)
    limit = request.args.get("limit", 5)
    query = request.args.get("query", "")

    return {
        "result": [{**rest.dict(), "owner": rest.owner.username} for rest in
                   Restaurant.query.filter(Restaurant.name.like(f"%{query}%")).offset(start).limit(limit).all()]
    }
