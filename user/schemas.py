from typing import List, Union, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    login: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# will be used when reading data, when returning it from the API.
class UserDetail(UserBase):
    user_id: int

    class Config:
        orm_mode = True
