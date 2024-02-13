import os
from typing import List

from src.auth.jwt import get_current_user
from src.image.utils import author_or_not, delete_image
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from src.database import get_async_session
from src.image.shemas import SuccessResponse, ImageNameSuccess, SuccessImageResponse
from src.image.utils import generate_filename, save_photo, delete_photo
from src.posts.model import Image

router = APIRouter(
    prefix='/image',
    tags=['Image']
)


@router.post('', response_model=SuccessImageResponse, dependencies=[Depends(author_or_not)])
async def post_image(post_id: int, files: List[UploadFile] = File(), session: AsyncSession = Depends(get_async_session),
                     current_user=Depends(get_current_user)):
    try:
        filenames = []
        for index, element in enumerate(files):
            if not element.filename:
                break
            filename = generate_filename(element.filename)
            save_photo(filename, element.file)
            stmt = insert(Image).values(filename=filename, post_id=post_id)
            await session.execute(stmt)
            filenames.append(filename)
        await session.commit()
        return {'status': 200, 'data': filenames}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.get('/{post_id}', response_model=ImageNameSuccess)
async def get_imagename(post_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Image).where(Image.post_id == post_id)
    result = await session.execute(stmt)
    return {'status': 200, 'data': result.scalars().all()}


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


@router.put('', dependencies=[Depends(author_or_not), Depends(delete_image)], response_model=SuccessImageResponse)
async def put_image(post_id: int, session: AsyncSession = Depends(get_async_session), files: List[UploadFile] = File(),
                    current_user=Depends(get_current_user)):
    filenames = []
    for index, element in enumerate(files):
        if not element.filename:
            break
        filename = generate_filename(element.filename)
        save_photo(filename, element.file)
        stmt = insert(Image).values(filename=filename, post_id=post_id)
        filenames.append(filename)

        await session.execute(stmt)
    await session.commit()
    return {'status': 200, 'data': filenames}


@router.delete('', dependencies=[Depends(author_or_not), Depends(delete_image)], response_model=SuccessResponse)
async def delete_image(post_id: int, session: AsyncSession = Depends(get_async_session), current_user=Depends(get_current_user)):
    return {'status': 200}
