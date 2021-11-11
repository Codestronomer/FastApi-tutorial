from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True





class UserCreate(UserBase):
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
