import time
import os
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_db(database_url, max_retries=None, retry_interval=None):
    """
    Wait for the database to be ready with configurable retry logic
    """
    max_retries = max_retries or int(os.getenv("MAX_DB_RETRIES", "5"))
    retry_interval = retry_interval or int(os.getenv("DB_RETRY_INTERVAL", "5"))
    
    for attempt in range(max_retries):
        try:
            if database_url.startswith('redis'):
                # Import Redis only when needed
                import redis
                
                # Parse Redis URL
                host = os.getenv("REDIS_HOST", "localhost")
                port = int(os.getenv("REDIS_PORT", "6379"))
                password = os.getenv("REDIS_PASSWORD", "")
                
                # Create Redis connection
                client = redis.Redis(
                    host=host,
                    port=port,
                    password=password,
                    decode_responses=True
                )
                # Test the connection
                client.ping()
                logger.info("Successfully connected to Redis")
                return client
            else:
                # Create PostgreSQL connection
                engine = create_engine(database_url)
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                    conn.commit()
                logger.info("Successfully connected to PostgreSQL")
                return engine
                
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                logger.error("Failed to connect to the database after maximum retries")
                raise e
