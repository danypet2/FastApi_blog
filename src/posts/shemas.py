from pydantic import BaseModel
from datetime import datetime


class PostShemas(BaseModel):
    title: str
    content: str
    image: str
