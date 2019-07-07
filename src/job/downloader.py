import os
import sys

import redis
from rq import Worker, Queue, Connection

listen = ['default']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
# redis_url = 'redis://teris:Mz5nDwQVT9h3lQa0pEI3vYMKNZNnO1Nr@redis-10454.c44.us-east-1-2.ec2.cloud.redislabs.com:10454'
conn = redis.from_url(redis_url)
