from typing import List

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status: int = 200


class SuccessImageResponse(BaseModel):
    status: int = 200
    data: List[str] = None


class ImageName(BaseModel):
    filename: str
    id: int
    post_id: int


class ImageNameSuccess(BaseModel):
    status: int = 200
    data: List[ImageName]