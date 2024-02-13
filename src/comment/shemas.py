from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime



#request
class CommentShemas(BaseModel):
    comment: str


#response
class Comment(BaseModel):
    data_updated: Optional[datetime] = None
    author_id: int
    id: int
    post_id: int
    comment: str
    data_published: datetime

class ListCommentResponse(BaseModel):
    status: int
    data: List[Comment]

class SuccessResponse(BaseModel):
    status: int = 200


class SuccessResponseComment(BaseModel):
    status: int = 200
    data: Comment