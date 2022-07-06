from app.service.db import db
from app.db_models.user import User


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    ownerId = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    reviews = db.relationship("Review", cascade="all, delete")
