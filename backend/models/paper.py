from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaperCreate(BaseModel):
    user_id: str
    title: str
    file_url: str


class PaperResponse(BaseModel):
    id: str
    user_id: str
    title: str
    file_url: str
    uploaded_at: Optional[datetime] = None
