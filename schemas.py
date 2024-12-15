"""
    Validation schemas
"""

from typing import List
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    """
        Base model for post schemas
    """
    title: str
    content: str


class PostCreate(PostBase):
    """
        Create model for post schemas
    """

class Post(PostBase):
    """ 
        Model for post schemas
    """
    id: int
    owner_id: int

    class Config:
        """
            Config
        """
        orm_mode = True

class UserBase(BaseModel):
    """
        Base model for user schemas
    """
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """
        Create model for user schemas
    """

class User(UserBase):
    """
        Model for user schemas
    """
    id: int
    posts: List[Post] = []

    class Config:
        """
            Config
        """
        orm_mode = True
