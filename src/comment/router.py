from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import insert, select, update, delete, desc, nullslast
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from sqlalchemy.sql.functions import coalesce

from src.auth.model import User
from src.auth.jwt import get_current_user
from src.comment.model import Comment
from src.comment.shemas import CommentShemas, ListCommentResponse, SuccessResponse, SuccessResponseComment
from src.comment.utils import post_or_not, author_or_read_only
from src.database import get_async_session

router = APIRouter(
    prefix='/comment',
    tags=['Comment']
)


@router.post('/{post_id}', dependencies=[Depends(post_or_not)], response_model=SuccessResponseComment)
async def add_comment(post_id: int, comment: CommentShemas, session: AsyncSession = Depends(get_async_session),
                      current_user=Depends(get_current_user)):
    try:
        stmt = insert(Comment).values(comment=comment.comment, author_id=current_user.id, post_id=post_id).returning(
            Comment)
        result = await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'data': result.scalar()}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.get('/{post_id}', dependencies=[Depends(post_or_not)], response_model=ListCommentResponse)
@cache(expire=100)
async def get_comment(post_id: int, session: AsyncSession = Depends(get_async_session), page: int = 0, limit: int = 50):
    try:
        stmt = select(Comment).where(Comment.post_id == post_id).offset(
            page).limit(limit).order_by(
            desc(
                coalesce(Comment.data_updated, Comment.data_published)
            )
        )
        result = await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'data': result.scalars().all()}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.put('/{comment_id}', dependencies=[Depends(author_or_read_only)], response_model=SuccessResponseComment)
async def update_comment(comment_id: int, comment: CommentShemas, session: AsyncSession = Depends(get_async_session),
                         current_user=Depends(get_current_user)):
    try:
        stmt = update(Comment).where(Comment.id == comment_id).values(comment=comment.comment).returning(Comment)
        result = await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'data': result.scalar()}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.delete('/{comment_id}', dependencies=[Depends(author_or_read_only)], response_model=SuccessResponse)
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_async_session),
                         current_user=Depends(get_current_user)):
    try:
        stmt = delete(Comment).where(Comment.id == comment_id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 200}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
