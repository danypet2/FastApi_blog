from sqlalchemy import Column, Integer, String, ForeignKey

from src.database import Base
from src.posts.model import Post


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String)
    post_id = Column(Integer, ForeignKey(Post.id), nullable=True)