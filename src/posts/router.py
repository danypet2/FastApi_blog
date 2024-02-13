from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, delete, update, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.auth.shemas import UserRead
from src.image.utils import  delete_image
from src.database import get_async_session
from src.posts.model import Post, Image
from src.posts.shemas import PostShemas, SuccessResponse, SuccessResponsePosts, SuccessResponsePost
from fastapi_cache.decorator import cache
from src.posts.utils import post_or_not, delete_comment, author_or_not

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('', response_model=SuccessResponsePosts)
@cache(expire=100)
async def get_posts(session: AsyncSession = Depends(get_async_session),
                    page: int = 0, limit: int = 50):
    try:
        stmt = select(Post).offset(
            page).limit(limit).order_by(desc(Post.data_updated if not Post.data_updated else Post.data_published))
        result = await session.execute(stmt)
        return {'status': 200, 'data': result.scalars().all()}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.get('/{post_id}', response_model=SuccessResponsePost, dependencies=[Depends(post_or_not)])
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                   ):
    try:
        stmt = select(Post).where(Post.id == post_id)
        result = await session.execute(stmt)
        return {'status': 200, 'data': result.scalar()}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.post('', response_model=SuccessResponsePost)
async def add_post(new_post: PostShemas,
                   session: AsyncSession = Depends(get_async_session),
                   current_user=Depends(get_current_user)):
    try:
        stmt = insert(Post).values(title=new_post.title, content=new_post.content,
                                   author_id=current_user.id).returning(Post)
        result = await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'data': result.scalar()}

    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.delete('/{post_id}', dependencies=[Depends(author_or_not), Depends(delete_image), Depends(delete_comment)], response_model=SuccessResponse)
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                      current_user: UserRead = Depends(get_current_user),
                      ):
    try:
        stmt_post = delete(Post).where(Post.id == post_id).where(Post.author_id == current_user.id)
        await session.execute(stmt_post)

        await session.commit()
        return {'status': 200}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.put('/{post_id}', dependencies=[Depends(author_or_not)], response_model=SuccessResponsePost)
async def put_post(post_id: int, new_post: PostShemas,
                   session: AsyncSession = Depends(get_async_session),
                   current_user: UserRead = Depends(get_current_user)):
    try:

        stmt_post = update(Post).where(Post.id == post_id).where(Post.author_id == current_user.id).values(
            title=new_post.title, content=new_post.content,
            author_id=current_user.id).returning(Post)
        result = await session.execute(stmt_post)
        await session.commit()
        return {'status': 200, 'data': result.scalar()}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
