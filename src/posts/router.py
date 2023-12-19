from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.model import Post
from src.posts.shemas import PostShemas

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('')
async def get_posts(session: AsyncSession = Depends(get_async_session), page: int = 0, limit: int = 50):
    query = select(Post).offset(page).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get('/{post_id}')
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    return result.scalar()


@router.post('/add_post')
async def add_post(new_post: PostShemas, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Post).values(**new_post.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 200, 'data': new_post}
