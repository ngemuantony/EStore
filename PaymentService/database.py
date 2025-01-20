from redis_om import get_redis_connection

# Redis connection
redis = get_redis_connection(
    host="localhost",  # Redis host
    port=6379,        # Redis port
    decode_responses=True
)
