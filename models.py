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
    posts = relationship('Post', back_populates='owner', cascade='all, delete')

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email})'

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

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, user_id={self.user_id})'
