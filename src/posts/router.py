from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, delete, update, join
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.auth.model import User
from src.auth.shemas import UserRead
from src.auth.utils import user_post
from src.database import get_async_session
from src.posts.model import Post
from src.posts.shemas import PostShemas
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('')
@cache(expire=180)
async def get_posts(session: AsyncSession = Depends(get_async_session),
                    page: int = 0, limit: int = 50):
    try:
        stmt = select(Post, User.username).join(User, Post.author_id == User.id).offset(page).limit(limit)
        result = await session.execute(stmt)
        data = []
        for post, username in result.all():
            post.username = username
            data.append({'post': post})
        return {'status': 200, 'data': data}

    except:
        raise HTTPException(status_code=400, detail='Unknown error')


@router.get('/{post_id}')
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                   ):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Пост не найден')
    try:
        query = select(Post).where(Post.id == post_id)
        result = await session.execute(query)
        return {'status': 200, 'data': result.scalar()}
    except:
        raise HTTPException(status_code=400, detail='Unknown error')


@router.post('/add_post')
async def add_post(new_post: PostShemas, session: AsyncSession = Depends(get_async_session),
                   current_user=Depends(get_current_user)):
    try:
        stmt = insert(Post).values(title=new_post.title, content=new_post.content, image=new_post.image,
                                   author_id=current_user.id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'data': new_post}
    except:
        raise HTTPException(status_code=400, detail='Unknown error')


@router.delete('/{post_id}')
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                      current_user=Depends(get_current_user),
                      auth_check=Depends(user_post)):
    try:
        stmt = delete(Post).where(Post.id == post_id).where(Post.author_id == current_user.id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 200}
    except:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')


@router.put('/{post_id}')
async def put_post(post_id: int, new_post: PostShemas, session: AsyncSession = Depends(get_async_session),
                   current_user=Depends(get_current_user), auth_check=Depends(user_post)):
    try:
        stmt = update(Post).where(Post.id == post_id).where(Post.author_id == current_user.id).values(**new_post.dict())
        await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'data': new_post}
    except:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')
