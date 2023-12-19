from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(40))
    content = Column(String(10000))
    image = Column(String(1000))
    data_published = Column(DateTime(timezone=True), server_default=func.now())
    data_updated = Column(DateTime(timezone=True), onupdate=func.now())
