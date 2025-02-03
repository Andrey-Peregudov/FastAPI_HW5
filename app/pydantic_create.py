from pydantic import BaseModel
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None


class CarCreate(BaseModel):
    model: str
    year: Optional[int] = None
