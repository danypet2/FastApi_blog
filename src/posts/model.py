from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from src.auth.model import User

from src.database import Base


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(40), nullable=False)
    content = Column(String(10000), nullable=False)
    data_published = Column(DateTime(timezone=True), server_default=func.now())
    data_updated = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey(User.id), nullable=False)
