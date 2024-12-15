"""
    CRUD operations for the web app
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User, Post


def create_user(session: Session, username: str, email: str, password: str):
    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()
    return new_user


def create_post(session: Session, title: str, content: str, user_id: int):
    new_post = Post(title=title, content=content, user_id=user_id)
    session.add(new_post)
    session.commit()
    return new_post


def get_user(session: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    return session.scalars(stmt).one_or_none()


def get_post(session: Session, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    return session.scalars(stmt).one_or_none()


def get_all_users(session: Session):
    stmt = select(User)
    return session.scalars(stmt).all()

def get_all_posts(session: Session):
    stmt = select(Post)
    return session.scalars(stmt).all()

def edit_user(session: Session, user_id: int, new_username: str, new_email: str, new_password: str):
    stmt = select(User).where(User.id == user_id)
    user = session.scalars(stmt).one()
    user.username = new_username
    user.email = new_email
    user.password = new_password
    session.commit()
    return user

def edit_post(session: Session, post_id: int, new_title: str, new_content: str):
    stmt = select(Post).where(Post.id == post_id)
    post = session.scalars(stmt).one()
    post.title = new_title
    post.content = new_content
    session.commit()
    return post

def delete_user(session: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    user = session.scalars(stmt).one()
    session.delete(user)
    session.commit()
    return user

def delete_post(session: Session, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    post = session.scalars(stmt).one()
    session.delete(post)
    session.commit()
    return post
