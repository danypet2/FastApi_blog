from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.auth.model import User
from src.database import get_async_session
from src.message.model import Message
from src.message.shemas import MessageShemas


async def author_or_read_only(message_id: int, session: AsyncSession = Depends(get_async_session),
                              current_user=Depends(get_current_user)):
    message = await session.get(Message, message_id)

    if not message:
        raise HTTPException(status_code=400, detail='Сообщение не найдено')
    if not(message.user_id == current_user.id):
        raise HTTPException(status_code=400, detail='Вы не являетесь автором сообщение')

async def user_or_not(message: MessageShemas, session: AsyncSession = Depends(get_async_session)):
    user_id = message.to_user_id
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

async def user_or_not_id(to_user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_id = to_user_id
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')