from redis import asyncio as redis
from app.settings.db_settings import settings

port = settings.redis_config.REDIS_PORT
host = settings.redis_config.REDIS_HOST
bd = settings.redis_config.REDIS_BD

redis = redis.Redis(host=host, port = port)
