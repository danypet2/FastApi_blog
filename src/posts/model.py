from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.auth.model import User
from src.database import Base


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(40))
    content = Column(String(10000))
    image = Column(String(1000))
    data_published = Column(DateTime(timezone=True), server_default=func.now())
    data_updated = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey(User.id))
    image_id = Column(Integer, ForeignKey('image.id'), nullable=False)


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String)



