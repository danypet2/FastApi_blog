from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from src.auth.jwt import get_current_user
from src.database import get_async_session
from src.message.model import Message
from src.message.shemas import MessageShemas, MessageListResponse, SuccessResponse, MessageResponseOne
from src.message.utils import author_or_read_only, user_or_not, user_or_not_id

router = APIRouter(
    tags=['Message'],
    prefix='/message'
)


@router.post('', response_model=MessageResponseOne, dependencies=[Depends(user_or_not)])
async def message_post(message: MessageShemas, session: AsyncSession = Depends(get_async_session),
                       current_user=Depends(get_current_user)):
    try:
        stmt = insert(Message).values(user_id=current_user.id, to_user_id=message.to_user_id,
                                      content=message.content).returning(Message)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Пользователь не найден')
    try:
        result = await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'data': result.scalar()}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.get('/{to_user_id}', response_model=MessageListResponse, dependencies=[Depends(user_or_not_id)])
async def message_get(to_user_id: int, session: AsyncSession = Depends(get_async_session),
                      current_user=Depends(get_current_user)):
    try:
        result = await session.execute(
            text(
                f'''
                SELECT * 
                FROM( SELECT * 
                FROM MESSAGE WHERE MESSAGE.user_id = {current_user.id} AND MESSAGE.to_user_id = {to_user_id}
                UNION SELECT * 
                FROM MESSAGE WHERE MESSAGE.to_user_id = {current_user.id} AND MESSAGE.user_id = {to_user_id}) 
                T 
                ORDER BY coalesce (data_updated, data_send)
                '''
            )
        )
        return {'status': 200, 'data': [dict(r._mapping) for r in result]}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.put('/{message_id}', dependencies=[Depends(author_or_read_only)], response_model=MessageResponseOne)
async def put_message(message_id: int, message: MessageShemas, session: AsyncSession = Depends(get_async_session),
                      current_user=Depends(get_current_user)):
    try:
        stmt = update(Message).where(Message.id == message_id).values(user_id=current_user.id,
                                                                      to_user_id=message.to_user_id,
                                                                      content=message.content).returning(Message)
        result = await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'data': result.scalar()}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.delete('{message_id}', dependencies=[Depends(author_or_read_only)], response_model=SuccessResponse)
async def delete_message(message_id: int, session: AsyncSession = Depends(get_async_session),
                         current_user=Depends(get_current_user)):
    try:
        stmt = delete(Message).where(Message.id == message_id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 200}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
