from app.core.redis import redis_client


def clear_dashboard_cache(user_id: int):
    pattern = f"dashboard:{user_id}:*"
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)