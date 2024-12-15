"""
    Meant to used as a script, can do different syncronous opeartions with the database
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from faker import Faker

from database import sync_session, engine
from models import Base, Post, User

fake = Faker()

async def startup():
    """
        Syncs db if needed, returns a session
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return Session(engine)

def create_some_users(session: Session):
    """
        Creates random users and adds them to the db
    """
    new_users = [User(username=fake.user_name(), email=fake.email(), password=fake.password()) for _ in range(10)]
    session.add_all(new_users)
    session.commit()


def create_some_posts(session: Session):
    """
        Creates a random post for each user in the db, but only up to 10 users
    """
    stmt = select(User).limit(10)
    users = session.scalars(stmt).all()
    for user in users:
        new_post = Post(title=fake.sentence(), content=fake.text(), owner=user)
        session.add(new_post)
    session.commit()

def get_all_users(session: Session):
    """
        Returns all users in the db
    """
    stmt = select(User)
    return session.scalars(stmt).all()

def get_all_posts_with_owners(session: Session):
    """
        Returns all posts in the db with their owners
    """
    stmt = select(Post).join(Post.owner)
    return session.scalars(stmt).all()

def get_posts_of_user(session: Session, user_id: int):
    """
        Returns all posts of a user
    """
    stmt = select(Post).where(Post.user_id == user_id)
    return session.scalars(stmt).all()

def update_email(session: Session, user_id: int, new_email: str):
    """
        Updates the email of a user
    """
    stmt = select(User).where(User.id == user_id)
    user = session.scalars(stmt).one()
    user.email = new_email
    session.commit()

def update_post_content(session: Session, post_id: int, new_content: str):
    """
        Updates the content of a post
    """
    stmt = select(Post).where(Post.id == post_id)
    post = session.scalars(stmt).one()
    post.content = new_content
    session.commit()

def delete_post(session: Session, post_id: int):
    """
        Deletes a post
    """
    stmt = select(Post).where(Post.id == post_id)
    post = session.scalars(stmt).one()
    session.delete(post)
    session.commit()

def delete_user(session: Session, user_id: int):
    """
        Deletes a user and their posts
    """
    stmt = select(User).where(User.id == user_id)
    user = session.scalars(stmt).one()
    # because of the cascade delete, the posts will be deleted as well
    session.delete(user)
    session.commit()


call_tree = {
    "create_some_users": {
        "function": create_some_users,
        "args": [],
    },
    "create_some_posts": {
        "function": create_some_posts,
        "args": [],
    },
    "get_all_users": {
        "function": get_all_users,
        "args": [],
    },
    "get_all_posts_with_owners": {
        "function": get_all_posts_with_owners,
        "args": [],
    },
    "get_posts_of_user": {
        "function": get_posts_of_user,
        "args": [int],
    },
    "update_email": {
        "function": update_email,
        "args": [int, str],
    },
    "update_post_content": {
        "function": update_post_content,
        "args": [int, str],
    },
    "delete_post": {
        "function": delete_post,
        "args": [int],
    },
    "delete_user": {
        "function": delete_user,
        "args": [int],
    },
}

if __name__ == "__main__":
    with sync_session() as session:
        while True:
            command = input("What do you want to do? Enter: ")
            if command == "quit":
                break
            elif command in call_tree:
                arg_types = call_tree[command]["args"]
            else:
                print("Invalid command. Here's a list available commands:")
                for command in call_tree:
                    print(command)
                print("Type 'quit' to exit.")
                continue
            if len(arg_types) == 0:
                res = call_tree[command]["function"](session)
                print(res)
            else:
                user_args = []
                for arg_type in arg_types:
                    user_args.append(arg_type(input("Enter argument: ")))
                res = call_tree[command]["function"](session, *user_args)
                print(res)
