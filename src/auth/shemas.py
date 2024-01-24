from pydantic import BaseModel, EmailStr, constr


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: constr(min_length=4, max_length=15)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    hashed_password: constr(min_length=8, max_length=20)




class RefreshToken(BaseModel):
    refresh_token: str


class UserCode(BaseModel):
    email: EmailStr
    code: int


class UserCodeReset(BaseModel):
    email: EmailStr
    code: int
    new_password: constr(min_length=8, max_length=20)


class EmailUser(BaseModel):
    email: EmailStr
