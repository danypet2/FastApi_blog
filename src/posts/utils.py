from fastapi import Depends, HTTPException
from sqlalchemy import delete

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.auth.shemas import UserRead
from src.comment.model import Comment
from src.database import get_async_session
from src.posts.model import Post


async def author_or_not(post_id: int, session: AsyncSession = Depends(get_async_session),
                        current_user: UserRead = Depends(get_current_user)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=400, detail='Данный пост не найден')
    if not (post.author_id == current_user.id):
        raise HTTPException(status_code=400, detail='Вы не являетесь автором этого поста')


async def post_or_not(post_id: int, session: AsyncSession = Depends(get_async_session),
                      current_user: UserRead = Depends(get_current_user)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=400, detail='Данный пост не найден')


async def delete_comment(post_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(Comment).where(Comment.post_id == post_id)
        await session.execute(stmt)
        await session.commit()
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
