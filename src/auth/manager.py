from typing import Optional
from src.auth.task import send_email_verification, send_email_forgot_password, send_email_after_registr, \
    send_email_after_verify
from fastapi_users import IntegerIDMixin, BaseUserManager, schemas, models, exceptions
from fastapi import Depends, Request, HTTPException
from src.auth.model import User, get_user_db
from src.config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        send_email_after_registr.delay(user.username, user.email)

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        send_email_verification.delay(user.username, user.email,
                                      token)  # Добавление в celery отправку письма для подтверждения почты

    async def on_after_forgot_password(
            self, user: models.UP, token: str, request: Optional[Request] = None
    ):
        send_email_forgot_password.delay(user.username, user.email,
                                         token)  # Добавление в celery отправку письма для сброса пароля

    async def on_after_verify(
            self, user: User, request: Optional[Request] = None
    ):
        send_email_after_verify.delay(user.username, user.email)

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict['role_id'] = 2

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
