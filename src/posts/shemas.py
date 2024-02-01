from typing import List, Optional, Union

from fastapi import Depends, UploadFile, File, Form
from pydantic import BaseModel
from datetime import datetime




class PostShemas(BaseModel):
    title: str
    content: str







# Optional[Union[UploadFile, List[UploadFile]]] = File(None)