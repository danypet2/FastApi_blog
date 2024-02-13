from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey

from src.auth.model import User
from src.database import Base
from src.posts.model import Post


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comment = Column(String(3000), nullable=False)
    data_published = Column(DateTime(timezone=True), server_default=func.now())
    data_updated = Column(DateTime(timezone=True), onupdate=func.now())

    author_id = Column(Integer, ForeignKey(User.id), nullable=False)
    post_id = Column(Integer, ForeignKey(Post.id), nullable=False)


