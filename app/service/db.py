from flask_sqlalchemy import SQLAlchemy
from app.domain.singleton import Singleton


class DB(SQLAlchemy, metaclass=Singleton):
    pass


db = DB()
