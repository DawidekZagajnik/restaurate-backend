from app.service.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    passHash = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String(20), nullable=False)
