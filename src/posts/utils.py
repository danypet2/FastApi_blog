from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import fastapi_users
from src.auth.model import User
from src.database import get_async_session
from src.posts.model import Post

current_user = fastapi_users.current_user()


async def author_or_read_only(post_id: int, session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Пост не найден')

    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail='Вы не являетесь автором этого поста')
