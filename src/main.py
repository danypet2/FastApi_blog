from fastapi import FastAPI, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.posts.shemas import PostShemas
from src.database import get_async_session
from src.posts.model import Post
from src.posts.router import router as router_post

app = FastAPI(title='social_netw')

app.include_router(router_post)
