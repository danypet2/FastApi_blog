import fastapi_users.router
from fastapi import FastAPI, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.base_config import fastapi_users
from src.auth.base_config import auth_backend
from src.auth.shemas import UserRead, UserCreate
from src.posts.shemas import PostShemas
from src.database import get_async_session
from src.posts.model import Post
from src.posts.router import router as router_post

app = FastAPI(title='social_netw')

app.include_router(router_post)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
