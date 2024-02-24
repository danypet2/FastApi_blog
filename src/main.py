from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.comment.router import router as router_comment
from src.posts.router import router as router_post
from src.image.router import router as router_image
from src.message.router import router as router_message
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as auth_router



app = FastAPI(title='social_netw')

app.include_router(router_post)
app.include_router(auth_router)
app.include_router(router_comment)
app.include_router(router_image)
app.include_router(router_message)
# app.include_router(router_popularity)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
