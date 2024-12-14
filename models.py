"""
    Defines models
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    """
        Base
    """

class User(Base):
    """
        User table
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
    posts = relationship('Post', back_populates='owner')

class Post(Base):
    """
        Post table
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    content = Column(String(2000))
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User')
