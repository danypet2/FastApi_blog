from typing import Optional
from passlib.context import CryptContext
from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(BaseModel):
    email: str
    username: str
    hashed_password: str
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False

