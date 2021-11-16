from typing import Optional
from pydantic import BaseModel, ValidationError
from datetime import datetime
from pydantic.networks import EmailStr
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserBase(BaseModel):
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


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True



# data = {
#         "Post": {
#             "title": "post2",
#             "content": " di vo job wdbon dbos",
#             "created": "2021-11-10T18:55:10.455945+00:00",
#             "published": True,
#             "id": 4,
#             "owner_id": 11
#         },
#         "votes": 2
#     }

# try:
#     PostOut(**data)
# except ValidationError as e:
#     print(e.json())






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


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)