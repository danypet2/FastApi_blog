from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MessageShemas(BaseModel):
    to_user_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    user_id: int
    to_user_id: int
    content: str
    data_send: Optional[datetime] = None
    data_updated: Optional[datetime] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MessageListResponse(BaseModel):
    status: int = 200
    data: Optional[List[MessageResponse]] = None

    class Config:
        from_attributes = True


class MessageResponseOne(BaseModel):
    status: int = 200
    data: MessageResponse


class SuccessResponse(BaseModel):
    status: int = 200
