from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy import func
from src.auth.model import User
from src.database import Base


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    to_user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    content = Column(String(3000), nullable=False)
    data_send = Column(DateTime(timezone=True), server_default=func.now())
    data_updated = Column(DateTime(timezone=True), onupdate=func.now())
