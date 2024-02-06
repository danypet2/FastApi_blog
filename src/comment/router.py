from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.model import User
from src.comment.utils import author_or_read_only, post_or_not
from src.auth.jwt import get_current_user
from src.comment.model import Comment
from src.comment.shemas import CommentShemas, ListCommentResponse, SuccessResponse
from src.database import get_async_session

router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)


@router.post('/{post_id}', dependencies=[Depends(post_or_not)], response_model=SuccessResponse)
async def add_comment(post_id: int, comment: CommentShemas, session: AsyncSession = Depends(get_async_session),
                      current_user=Depends(get_current_user)):
    try:
        stmt = insert(Comment).values(comment=comment.comment, author_id=current_user.id, post_id=post_id)
        result = await session.execute(stmt)
        await session.commit()
        return {'status': 200}
    except:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')


@router.get('/{post_id}', response_model=ListCommentResponse)
async def get_comment(post_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(Comment, User.username).where(Comment.post_id == post_id).join(User, Comment.author_id == User.id)
        result = await session.execute(stmt)
        data = []
        for result, username in result.all():
            setattr(result, 'username', username)
            data.append({'result': result})

        await session.commit()
        return {'status': 200, 'data': data}
    except:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')


@router.put('/{comment_id}', dependencies=[Depends(author_or_read_only)], response_model=SuccessResponse)
async def update_comment(comment_id: int, comment: CommentShemas, session: AsyncSession = Depends(get_async_session),
                         current_user=Depends(get_current_user)):
    stmt = update(Comment).where(Comment.id == comment_id).values(comment=comment.comment)
    await session.execute(stmt)
    await session.commit()
    return {'status': 200}


@router.delete('/{comment_id}', dependencies=[Depends(author_or_read_only)], response_model=SuccessResponse)
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_async_session),
                         current_user=Depends(get_current_user)):
    stmt = delete(Comment).where(Comment.id == comment_id)
    await session.execute(stmt)
    await session.commit()
    return {'status': 200}
