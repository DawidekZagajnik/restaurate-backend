from flask import Blueprint, request
from app.db_models import User, Review
from app.service.db import db
from app.domain.review_payload import ReviewPayload
from datetime import datetime
from app.utils.auth.auth_middleware import requires_auth
from pydantic import ValidationError


review_blueprint = Blueprint("review_endpoints", __name__, template_folder=None)


@review_blueprint.route("/review/<id>", methods=["DELETE"])
@requires_auth()
def delete_review(curr_user: User, id: int):
    result = Review.query.get(id)
    if not result:
        return f"Review with ID {id} not found.", 404

    if curr_user.id != result.userId:
        return f"You can remove only your reviews.", 409

    db.session.delete(result)
    db.session.commit()
    return {"deleted": 1}


@review_blueprint.route("/review", methods=["POST"])
@requires_auth()
def add_review(curr_user: User):
    try:
        payload = ReviewPayload(**request.json)
    except ValidationError as e:
        return str(e), 422

    review = Review(
        content=payload.content,
        rate=payload.rate,
        restaurantId=payload.restaurantId,
        timestamp=datetime.utcnow().timestamp(),
        userId=curr_user.id
    )

    db.session.add(review)
    db.session.commit()
    return {
        "inserted": {
            **review.dict(),
            "timestamp": datetime.utcfromtimestamp(review.timestamp).strftime("%Y-%m-%d %H:%M"),
            "user": review.user.username
        }
    }


@review_blueprint.route("/reviews/<restaurant_id>", methods=["GET"])
@requires_auth(return_user=False)
def load_reviews_for_restaurant(restaurant_id: int):
    page = int(request.args.get("page", "0"))
    pagesize = int(request.args.get("pagesize", "6"))

    result = Review.query.filter(Review.restaurantId == restaurant_id).order_by(Review.timestamp.desc())

    return {
        "result": [{
            **rest.dict(),
            "timestamp": datetime.utcfromtimestamp(rest.timestamp).strftime("%Y-%m-%d %H:%M"),
            "user": rest.user.username
        } for rest in result.offset(page * pagesize).limit(pagesize).all()],
        "has_more": result.count() > pagesize * page + pagesize
    }


@review_blueprint.route("/my-reviews", methods=["GET"])
@requires_auth()
def load_reviews_for_user(user: User):
    page = int(request.args.get("page", "0"))
    pagesize = int(request.args.get("pagesize", "6"))

    result = Review.query.filter(Review.userId == user.id).order_by(Review.timestamp.desc())

    return {
        "result": [{
            **rest.dict(),
            "timestamp": datetime.utcfromtimestamp(rest.timestamp).strftime("%Y-%m-%d %H:%M"),
            "user": user.username
        } for rest in result.offset(page * pagesize).limit(pagesize).all()],
        "has_more": result.count() > pagesize * page + pagesize
    }


