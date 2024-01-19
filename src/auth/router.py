import random
from datetime import timedelta, datetime
from src.auth.utils import redis_connect
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy import insert, select, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.jwt import get_password_hash, verify_password, create_access_token, REFRESH_TOKEN_EXPIRE_DAYS, \
    decode_access_token, get_current_user
from src.auth.model import User
from src.auth.shemas import UserCreate, UserRead
from src.auth.utils import random_code
from src.database import get_async_session
from src.auth.task import send_email_after_register, send_email_verification, send_email_after_verify, \
    email_forgot_password, send_email_forgot_password, send_email_after_reset_password

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
                                   is_active=True,
                                   is_superuser=False,
                                   is_verified=False
                                   )
        await session.execute(stmt)
        await session.commit()
        send_email_after_register.delay(data.username, data.email)
        return {'status': 200, 'detail': 'Регистрация прошла успешно'}

    except DBAPIError:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.post('/login')
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_async_session)):
    try:
        user = select(User).where(User.username == form_data.username)
        result = await session.execute(user)
        result = result.scalar()
    except:
        raise HTTPException(status_code=400, detail='Неизвестная ошибка')
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


@router.post('/verify_email')
async def verify_email(email_user: dict, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(User).where(User.email == email_user)
        result = await session.execute(stmt)
        result = result.scalar()
        if result and result.is_verified == False:
            random_code(email_user)
            send_email_verification.delay(email_user, redis_connect.get(email_user).decode())
            return {'status': 200}


    except:
        raise HTTPException(status_code=500)


@router.post('/verify_code')
async def verify_code(email: str, code: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if code == int(redis_connect.get(email).decode()):
            redis_connect.delete(email, code)
            stmt = update(User).where(User.email == email).values(is_verified=True)
            await session.execute(stmt)
            await session.commit()
            send_email_after_verify.delay(user_email=email)
            return {'status': 200}
        else:
            return {'status': 400}

    except:
        raise HTTPException(status_code=500)


@router.post('/forgot_password')
async def forgot_password(email: str, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        result = result.scalar()
        if not result:
            raise HTTPException(status_code=400, detail='Email не найден')
        random_code(email)
        send_email_forgot_password.delay(result.username, result.email, redis_connect.get(email).decode())
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.post('/reset_password')
async def reset_password(email: str, new_password: str, code: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if code == int(redis_connect.get(email).decode()):
            redis_connect.delete(email)
            stmt = update(User).where(User.email == email).values(hashed_password=get_password_hash(new_password))
            await session.execute(stmt)
            await  session.commit()
            send_email_after_reset_password.delay(email)
            return {'status': 200, 'detail': 'Ваш пароль успешно сброшен'}
        else:
            return dict(status_code=400, detail='Неправильный код доступа')
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')

