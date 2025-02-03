from pydantic import BaseModel
from typing import Optional, List



class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    cars: List[str]


class CarResponse(BaseModel):
    id: int
    model: str
    year: Optional[int]