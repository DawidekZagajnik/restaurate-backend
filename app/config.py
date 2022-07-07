import os
from app.domain.singleton import Singleton


class Config(metaclass=Singleton):

    def __init__(self):
        self.mysql_pass = os.environ.get("MYSQL_PASSWORD", "")
        self.mysql_username = os.environ.get("MYSQL_USERNAME", "")
        self.mysql_host = os.environ.get("MYSQL_HOST", "localhost")
        self.mysql_port = os.environ.get("MYSQL_PORT", 3306)
        self.mysql_database = os.environ.get("MYSQL_DATABASE", None)
        self.redis_host = os.environ.get("REDIS_HOST", "localhost")
        self.redis_pass = os.environ.get("REDIS_PASSWORD", None)
        self.redis_port = os.environ.get("REDIS_PORT", 6379)


config = Config()
