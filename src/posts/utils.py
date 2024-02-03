import os
import shutil
import uuid

from fastapi import Depends, HTTPException, File
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.auth.shemas import UserRead
from src.database import get_async_session
from src.posts.model import Post, Image
from src.posts.shemas import PostShemas


async def user_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                    current_user: UserRead = Depends(get_current_user)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=400, detail='Данный пост не найден')
    if not (post.author_id == current_user.id):
        raise HTTPException(status_code=400, detail='Вы не являетесь автором этого поста')


