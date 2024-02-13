from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.comment.model import Comment
from src.database import get_async_session
from src.posts.model import Post


async def post_or_not(post_id: int, session: AsyncSession = Depends(get_async_session), current_user = Depends(get_current_user)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=400, detail='Пост не найден')


async def author_or_read_only(comment_id: int, session: AsyncSession = Depends(get_async_session), current_user = Depends(get_current_user)):
    comment = await session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=400, detail='Пост не найден')
    if not (comment.author_id == current_user.id):
        raise HTTPException(status_code=400, detail='Вы не являетесь автором поста')