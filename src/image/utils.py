import os
import shutil
import uuid

from fastapi import Depends, HTTPException, File
from sqlalchemy import select, delete

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import get_current_user
from src.database import get_async_session
from src.posts.model import Post, Image



def save_photo(filename: str, image: File):
    try:
        upload_dir = os.path.join(os.getcwd(), 'static')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        dest = os.path.join(upload_dir, filename)
        with open(dest, 'wb') as buffer:
            shutil.copyfileobj(image, buffer)
    except:
        raise HTTPException(status_code=400, detail='Error save photo')


async def get_images_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt_image_filename = select(Image.filename).where(Image.post_id == post_id)
    image_filename = await session.execute(stmt_image_filename)
    image_filenames = image_filename.scalars().all()
    return image_filenames



async def author_or_not(post_id: int, session: AsyncSession = Depends(get_async_session), current_user = Depends(get_current_user)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=400, detail='Пост не найден')
    if not (post.author_id == current_user.id):
        raise HTTPException(status_code=400, detail='Вы не являетесь автором поста')

def delete_photo(images: list):
    try:
        if images:
            for image in images:
                upload_dir = os.path.join(os.getcwd(), 'static')
                path = os.path.join(upload_dir, image)
                os.remove(path)
        else:
            return True
    except:
        raise HTTPException(status_code=400, detail='Error delete photo')


def generate_filename(filename: str):
    if filename.rsplit('.')[-1] in ['jpeg', 'jpg', 'png']:
        return str(uuid.uuid4()) + '.' + filename.rsplit('.')[-1]
    raise HTTPException(status_code=400, detail='Разрешен только jpeg, jpg, png')


async def delete_image(post_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt_image_filename = select(Image.filename).where(Image.post_id == post_id)
        image_filename = await session.execute(stmt_image_filename)
        image_filenames = image_filename.scalars().all()
        delete_photo(image_filenames)
        stmt = delete(Image).where(Image.post_id == post_id)
        await session.execute(stmt)
        await session.commit()
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')