import redis
import json
import logging
from typing import Optional, Any
from app.config import settings
from datetime import timedelta

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        try:
            self.client = redis.from_url(
                settings.REDIS_URL,
                socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
                decode_responses=True
            )
            self.client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            self.client = None
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, expire_hours: int = 24) -> bool:
        try:
            self.client.setex(
                key,
                timedelta(hours=expire_hours),
                json.dumps(value)
            )
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {str(e)}")
            return False
    
    def get_free_credit(self, user_id: str) -> int:
        key = f"free_credit:{user_id}"
        credit = self.get(key)
        return credit if credit is not None else settings.FREE_CREDIT_LIMIT
    
    def set_free_credit(self, user_id: str, credit: int) -> bool:
        key = f"free_credit:{user_id}"
        return self.set(key, credit, expire_hours=settings.CREDIT_RESET_HOURS)

redis_client = RedisCache()