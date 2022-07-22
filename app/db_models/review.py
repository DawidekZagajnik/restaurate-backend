from app.service.db import db
from app.db_models.restaurant import Restaurant
from app.db_models.user import User
from flask_sqlalchemy import inspect


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    restaurantId = db.Column(db.Integer, db.ForeignKey(Restaurant.id))

    user = db.relationship("User", viewonly=True)
    restaurant = db.relationship("Restaurant", viewonly=True)

    def dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

