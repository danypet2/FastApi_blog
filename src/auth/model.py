from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import Column, String, Integer, DateTime, func, JSON, ForeignKey, Boolean
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base, get_async_session




class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)



class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'
    id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    email = Column(String(64), nullable=False)
    username = Column(String(30), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    role_id = Column(Integer, ForeignKey(Role.id))
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)




async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)




