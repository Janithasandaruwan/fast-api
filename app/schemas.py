from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import  Optional
from pydantic.types import conint

# Validate the request data*************************************** *****************************************************
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     #rating: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass



# Schema for create user************************************************************************************************
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Validate the response data********************************************************************************************
class PostResponse(PostBase):
    id: int
    created_at : datetime
    owner_id : int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

# Schema for user logging information***********************************************************************************
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for access token and  match************************************************************************************
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for the token data that embedded in to our access token********************************************************
class TokenData(BaseModel):
    id: Optional[str] = None

# Schema for vote to a post*********************************************************************************************
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)