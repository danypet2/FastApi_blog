import os.path
import shutil
from typing import List, Union, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import insert, select, delete, update, join
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from src.auth.jwt import get_current_user
from src.auth.model import User
from src.auth.shemas import UserRead
from src.comment.model import Comment
from src.image.utils import generate_filename, save_photo, delete_photo, get_images_post
from src.database import get_async_session
from src.posts.model import Post, Image
from src.posts.shemas import PostShemas, PostImageResponse, SuccessResponse
from fastapi_cache.decorator import cache
from src.posts.utils import user_post
from src.comment.shemas import ListCommentResponse


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('', response_model=PostImageResponse)
@cache(expire=1)
async def get_posts(session: AsyncSession = Depends(get_async_session),
                    page: int = 0, limit: int = 50):
    try:
        stmt = select(Post, User.username, Image.filename).join(User, Post.author_id == User.id).outerjoin(Image,
                                                                                                      Image.post_id == Post.id).offset(
            page).limit(limit)
        result = await session.execute(stmt)
        data = {}
        for post, username, image in result.all():
            if post.id not in data:
                data[post.id] = {'post': post, 'images': []}
            setattr(post, 'username', username)
            data[post.id]['images'].append(image)
        return {'status': 200, 'data': list(data.values())}
    except:
        raise HTTPException(status_code=404, detail='Неизвестная ошибка')


@router.get('/{post_id}', response_model=PostImageResponse)
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                   ):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Пост не найден')
    try:
        stmt = select(Post, User.username, Image.filename).where(Post.id == post_id).join(User,
                                                                                          Post.author_id == User.id).outerjoin(
            Image, Image.post_id == Post.id)
        result = await session.execute(stmt)
        data = {}
        for post, username, image in result.all():
            if post.id not in data:
                data[post.id] = {'post': post, 'images': []}
            setattr(post, 'username', username)
            data[post.id]['images'].append(image)
        return {'status': 200, 'data': list(data.values())}
    except:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')


@router.post('/add_post', response_model=SuccessResponse)
async def add_post(files: List[UploadFile] = File(), new_post: PostShemas = Depends(),
                   session: AsyncSession = Depends(get_async_session),
                   current_user=Depends(get_current_user)):
    try:
        stmt = insert(Post).values(title=new_post.title, content=new_post.content,
                                   author_id=current_user.id)
        result_id = await session.execute(stmt)
        result_id = result_id.inserted_primary_key[0]

        for index, element in enumerate(files):
            if not element.filename:
                break
            filename = generate_filename(element.filename)
            save_photo(filename, element.file)
            stmt = insert(Image).values(filename=filename, post_id=result_id)
            await session.execute(stmt)
        await session.commit()
        return {'status': 200}

    except:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')


@router.delete('/{post_id}', dependencies=[Depends(user_post)], response_model=SuccessResponse)
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                      current_user: UserRead = Depends(get_current_user),
                      images_post: list = Depends(get_images_post)):

        delete_photo(images_post)

        stmt = delete(Comment).where(Comment.post_id == post_id)
        await session.execute(stmt)

        stmt_image = delete(Image).where(Image.post_id == post_id)
        await session.execute(stmt_image)

        stmt_post = delete(Post).where(Post.id == post_id).where(Post.author_id == current_user.id)
        await session.execute(stmt_post)

        await session.commit()
        return {'status': 200}



@router.put('/{post_id}', dependencies=[Depends(user_post)], response_model=SuccessResponse)
async def put_post(post_id: int, files: List[UploadFile] = File(...), new_post: PostShemas = Depends(),
                   session: AsyncSession = Depends(get_async_session),
                   current_user: UserRead = Depends(get_current_user),
                   images_post: list = Depends(get_images_post)):
    try:
        delete_photo(images_post)
        delete_filename = delete(Image).where(Image.post_id == post_id)
        await session.execute(delete_filename)

        stmt_post = update(Post).where(Post.id == post_id).where(Post.author_id == current_user.id).values(
            title=new_post.title, content=new_post.content,
            author_id=current_user.id)
        await session.execute(stmt_post)

        for index, element in enumerate(files):
            if not element.filename:
                break
            filename = generate_filename(element.filename)
            save_photo(filename, element.file)
            stmt = insert(Image).values(filename=filename, post_id=post_id)
            await session.execute(stmt)
        await session.commit()
        return {'status': 200}
    except:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')


@router.get('/get_image/{filename}')
async def get_image(filename: str):
    try:
        file = os.path.join('static', filename)
        if os.path.exists(file):
            return FileResponse(file)
        else:
            return HTTPException(status_code=404, detail='Файл не найден')
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
