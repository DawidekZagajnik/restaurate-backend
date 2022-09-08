from flask import Blueprint
from app.db_models import Like, User
from app.service.db import db
from app.utils.auth.auth_middleware import requires_auth

like_blueprint = Blueprint("like_endpoints", __name__, template_folder=None)


@like_blueprint.route("/like/<review_id>", methods=["POST"])
@requires_auth()
def add_like(curr_user: User, review_id: int):

    if not Like.query.filter(Like.userId == curr_user.id and Like.reviewId == review_id).all():
        like = Like(
            reviewId=review_id,
            userId=curr_user.id
        )
        db.session.add(like)
        db.session.commit()
        return {"inserted": 1}

    else:
        return "You already liked this review.", 400


@like_blueprint.route("/like/<review_id>", methods=["DELETE"])
@requires_auth()
def delete_like(curr_user: User, review_id: int):
    if not (likes := Like.query.filter(Like.userId == curr_user.id and Like.reviewId == review_id).all()):
        return "This review is not liked by you.", 404

    else:
        db.session.delete(likes.pop())
        db.session.commit()
        return {"deleted": 1}


@like_blueprint.route("/likes/<review_id>", methods=["GET"])
@requires_auth()
def get_like_count(curr_user: User, review_id: int):
    return {
        "likes": Like.query.filter(Like.reviewId == review_id).count(),
        "liked": bool(Like.query.filter(Like.userId == curr_user.id and Like.reviewId == review_id).all())
    }

