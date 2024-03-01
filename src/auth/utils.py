import random
import redis

from src.config import REDIS_HOST, REDIS_PORT


def random_code(email_user, expire_minutes=5):
    code = random.randint(100000, 999999)
    email = email_user
    redis_connect.set(email, code, ex=expire_minutes*60)




redis_connect = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
