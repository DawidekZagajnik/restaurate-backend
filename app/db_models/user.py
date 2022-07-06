from app.service.db import db
from flask_sqlalchemy import inspect


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    passHash = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String(20), nullable=False)

    reviews = db.relationship("Review", cascade="all, delete", foreign_keys="Review.userId")
    restaurant = db.relationship("Restaurant", cascade="all, delete", foreign_keys="Restaurant.ownerId")

    def dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
