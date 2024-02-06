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
    username: str


class PostImage(BaseModel):
    post: PostResponse
    images: List[Optional[str]] = None

class PostImageResponse(BaseModel):
    status: int
    data: List[PostImage]


class SuccessResponse(BaseModel):
    status: int = 200