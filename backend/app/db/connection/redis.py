import redis.asyncio as redis

from app.config import getSettings

class RedisManager:
    """
    A class that implements the necessary functionality for working with Redis:
    managing connections and providing access to the Redis client.
    """

    def __init__(self, redis_url: str) -> None:
        self.redis_url = redis_url
        self.redis = None

    async def connect(self) -> None:
        """Connect to Redis."""
        self.redis = redis.from_url(self.redis_url)

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()

    def get_redis(self):
        """Get the Redis client."""
        return self.redis

settings = getSettings()
redis_manager = RedisManager(redis_url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
