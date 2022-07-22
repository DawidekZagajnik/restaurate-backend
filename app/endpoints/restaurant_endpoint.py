from flask import Blueprint, request
from app.db_models import Restaurant, User
from app.service.db import db
from app.domain.restaurant_payload import RestaurantPayload
from app.utils.auth.auth_middleware import requires_auth
from pydantic import ValidationError

restaurant_blueprint = Blueprint("restaurant_endpoints", __name__, template_folder=None)


@restaurant_blueprint.route("/restaurant/<id>", methods=["DELETE"])
@requires_auth()
def delete_restaurant(curr_user: User, id: int):
    result = Restaurant.query.get(id)
    if not result:
        return f"Restaurant with ID {id} not found.", 404

    if curr_user.id != result.ownerId:
        return f"You can delete only your restaurant.", 409

    db.session.delete(result)
    db.session.commit()

    return {"deleted": 1}


@restaurant_blueprint.route("/restaurant/<id>", methods=["GET"])
@requires_auth(return_user=False)
def get_restaurant(id: int):
    result = Restaurant.query.get(id)
    if not result:
        return f"Restaurant with ID {id} not found.", 404
    return {**result.dict(), "owner": result.owner.username}


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
@requires_auth(return_user=False)
def load_restaurants():
    page = int(request.args.get("page", "0"))
    pagesize = int(request.args.get("pagesize", "6"))
    query = request.args.get("query", "")

    result = Restaurant.query.filter(Restaurant.name.like(f"%{query}%"))

    return {
        "result": [{**rest.dict(), "owner": rest.owner.username} for rest in
                   result.offset(page * pagesize).limit(pagesize).all()],
        "has_more": result.count() > pagesize * page + pagesize
    }


@restaurant_blueprint.route("/restaurants/user/<id>", methods=["GET"])
@requires_auth(return_user=False)
def load_restaurant_of_user(id: int):
    page = int(request.args.get("page", "0"))
    pagesize = int(request.args.get("pagesize", "6"))

    result = Restaurant.query.filter(Restaurant.ownerId == id).order_by(Restaurant.id.desc())

    return {
        "result": [{**rest.dict(), "owner": rest.owner.username} for rest in
                   result.offset(page * pagesize).limit(pagesize).all()],
        "has_more": result.count() > pagesize * page + pagesize
    }
