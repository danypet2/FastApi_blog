from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy import insert, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.jwt import get_password_hash, verify_password, create_access_token, REFRESH_TOKEN_EXPIRE_DAYS, \
    decode_access_token
from src.auth.model import User
from src.auth.shemas import UserCreate
from src.database import get_async_session

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/register')
async def register_user(data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        existing_user = await session.execute(select(User).where(User.email == data.email))
        user_username = await session.execute(select(User).where(User.username == data.username))
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='Пользователь с таким email уже существует')
        if user_username.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='Данный никнейм занят')
        stmt = insert(User).values(email=data.email,
                                   username=data.username,
                                   hashed_password=get_password_hash(data.hashed_password),
                                   is_active=data.is_active,
                                   is_superuser=data.is_superuser,
                                   is_verified=data.is_verified
                                   )
        await session.execute(stmt)
        await session.commit()
        return {'status': 200, 'detail': 'Регистрация прошла успешно'}

    except DBAPIError:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')


@router.post('/login')
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_async_session)):
    user = select(User).where(User.username == form_data.username)
    result = await session.execute(user)
    result = result.scalar()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if verify_password(form_data.password, result.hashed_password):
        access_token = create_access_token(
            data={"sub": result.username}, expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_access_token(
            data={"sub": result.username}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post('/refresh_token')
async def refresh(refresh_token: str):
    try:
        decoded_token = decode_access_token(refresh_token)
        expiration_time = datetime.fromtimestamp(decoded_token['exp'])
        if expiration_time > datetime.utcnow():
            old_sub = decoded_token['sub']
            new_access_token = create_access_token(data={'sub': old_sub}, expires_delta=timedelta(minutes=15))
            return {'access_token': new_access_token}
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )