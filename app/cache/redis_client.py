import redis

from app.config import REDIS_URL


redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


def check_redis():
    return redis_client.ping()


def get_cached_answer(question: str):
    return redis_client.get(f"chat:{question}")


def set_cached_answer(question: str, answer: str, ttl: int = 3600):
    redis_client.setex(
        f"chat:{question}",
        ttl,
        answer,
    )
