from app.service.db import db
from app.db_models.user import User
from flask_sqlalchemy import inspect
from app.db_models.review import Review


class Like(db.Model):
    __tablename__ = "likes"

    reviewId = db.Column(db.Integer, db.ForeignKey(Review.id), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            reviewId, userId
        ),
    )

    def dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
