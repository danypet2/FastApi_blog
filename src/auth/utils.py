import random
import redis
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.auth.shemas import UserRead
from src.database import get_async_session
from src.posts.model import Post


def random_code(email_user, expire_minutes=5):
    code = random.randint(100000, 999999)
    email = email_user
    redis_connect.set(email, code, ex=expire_minutes*60)




redis_connect = redis.Redis(host='localhost', port=6379, db=0)
