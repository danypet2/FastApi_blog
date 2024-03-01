import random
import redis



def random_code(email_user, expire_minutes=5):
    code = random.randint(100000, 999999)
    email = email_user
    redis_connect.set(email, code, ex=expire_minutes*60)




redis_connect = redis.Redis(host='localhost', port=6379, db=0)
