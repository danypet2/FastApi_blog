from datetime import timedelta, datetime
from src.auth.utils import redis_connect
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy import insert, select, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.jwt import get_password_hash, verify_password, create_access_token, REFRESH_TOKEN_EXPIRE_DAYS, \
    decode_access_token
from src.auth.model import User
from src.auth.shemas import UserCreate, RefreshToken, UserCode, EmailUser, UserCodeReset, RegisterSuccess, LoginSuccess, \
    ResponseSuccess, ResponseReset, AccessToken, UserGetResponse
from src.auth.utils import random_code
from src.database import get_async_session
from src.auth.task import send_email_after_register, send_email_verification, send_email_after_verify, \
    send_email_forgot_password, send_email_after_reset_password

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register', response_model=RegisterSuccess)
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


@router.post('/login', response_model=LoginSuccess)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_async_session)):
    try:
        user = select(User).where(User.username == form_data.username)
        result = await session.execute(user)
        result = result.scalar()
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
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


@router.post('/refresh_token', response_model=AccessToken)
async def refresh(refresh_token: RefreshToken):
    try:
        decoded_token = decode_access_token(refresh_token.refresh_token)
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


@router.post('/verify_email', response_model=ResponseSuccess)
async def verify_email(data: EmailUser, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(User).where(User.email == data.email)
        result = await session.execute(stmt)
        result = result.scalar()
        if result and result.is_verified == False:
            random_code(data.email)
            send_email_verification.delay(data.email, redis_connect.get(data.email).decode())
            return {'status': 200}
        return {'status': 200}


    except:
        raise HTTPException(status_code=500, detail='123')


@router.post('/verify_code', response_model=ResponseSuccess)
async def verify_code(data: UserCode, session: AsyncSession = Depends(get_async_session)):
    if not redis_connect.get(data.email):
        return {'status': 200}
    if data.code == int(redis_connect.get(data.email).decode()):
        redis_connect.delete(data.email, data.code)
        try:
            stmt = update(User).where(User.email == data.email).values(is_verified=True)
            await session.execute(stmt)
            await session.commit()
            send_email_after_verify.delay(user_email=data.email)
            return {'status': 200}
        except:
            raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    elif not (data.code == int(redis_connect.get(data.email).decode())):
        raise HTTPException(status_code=401, detail='Код недействителен')



@router.post('/forgot_password/', response_model=ResponseSuccess)
async def forgot_password(data: EmailUser, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(User).where(User.email == data.email)
        result = await session.execute(stmt)
        result = result.scalar()
        if not result:
            return {'status': 200}

        random_code(data.email)
        send_email_forgot_password.delay(result.username, result.email, redis_connect.get(data.email).decode())
        return {'status': 200}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')


@router.post('/reset_password', response_model=ResponseReset)
async def reset_password(data: UserCodeReset, session: AsyncSession = Depends(get_async_session)):
    if not redis_connect.get(data.email):
        return {'status': 200}
    if data.code == int(redis_connect.get(data.email).decode()):
        try:
            redis_connect.delete(data.email)
            stmt = update(User).where(User.email == data.email).values(
                hashed_password=get_password_hash(data.new_password))
            await session.execute(stmt)
            await session.commit()
            send_email_after_reset_password.delay(data.email)
            return {'status': 200, 'detail': 'Ваш пароль успешно сброшен'}
        except:
            raise HTTPException(status_code=500, detail='Неизвестная ошибка')
    elif not (data.code == int(redis_connect.get(data.email).decode())):
        raise HTTPException(status_code=401, detail='Неправильный код доступа')



@router.get('{user_id}', response_model=UserGetResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(User.id, User.username, User.email).where(User.id == user_id)
    result = await session.execute(stmt)
    result = result.all()
    if not result:
        raise HTTPException(status_code=500, detail='Пользователь не найден')

    try:
        user = {}
        for user_id, user_username, user_email in result:
            user.update({'id': user_id, 'username': user_username, 'email': user_email})

        return {'status': 200, 'data': user}
    except:
        raise HTTPException(status_code=500, detail='Неизвестная ошибка')
