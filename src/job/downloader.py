import os
import sys

import redis
from rq import Worker, Queue, Connection

listen = ["default"]
redis_url = os.getenv("REDISCLOUD_URL", "redis://localhost:6379")
conn = redis.from_url(redis_url)
