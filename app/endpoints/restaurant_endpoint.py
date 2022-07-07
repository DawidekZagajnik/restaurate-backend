from flask import Blueprint, request
from app.db_models import Restaurant, User
from app.service.db import db
from app.domain.restaurant_payload import RestaurantPayload
from app.utils.auth.auth_middleware import requires_auth


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
    payload = RestaurantPayload(**request.json)
    restaurant = Restaurant(
        name=payload.name,
        description=payload.description,
        ownerId=curr_user.id
    )
    db.session.add(restaurant)
    db.session.commit()
    return {"inserted": 1}
