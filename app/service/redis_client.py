import redis
from app.domain.singleton import Singleton
from app.config import config


class RedisClient(metaclass=Singleton):

    def __init__(self, host: str, port: int, password: str):
        self.client = redis.Redis(
            host=host,
            port=port,
            password=password
        )


redis_client = RedisClient(config.redis_host, config.redis_port, config.redis_pass)
