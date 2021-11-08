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


class Post(PostBase):
    id: int
    created: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr



class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str