from typing import List, Optional, Union

from fastapi import Depends, UploadFile, File, Form
from pydantic import BaseModel, Field
from datetime import datetime

#request
class PostShemas(BaseModel):
    title: str
    content: str


#response
class PostResponse(BaseModel):
    title: str
    author_id: int
    content: str
    id: int
    data_updated: Optional[datetime] = None
    data_published: Optional[datetime] = None

class SuccessResponsePosts(BaseModel):
    status: int = 200
    data: List[PostResponse]

class SuccessResponsePost(BaseModel):
    status: int = 200
    data: PostResponse


class SuccessResponse(BaseModel):
    status: int = 200

