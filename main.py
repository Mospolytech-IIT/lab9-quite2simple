"""

    Main
"""


from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db_sync, engine
from models import Base, User

import crud


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    """

        Syncs db if needed
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/users", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db_sync)):
    users = crud.get_all_users(db)
    return templates.TemplateResponse("users/list.html", {"request": request, "users": users})


@app.post("/users/create", response_class=HTMLResponse)
def create_user(db: Session = Depends(get_db_sync), name: str = Form(...), email: str = Form(...)):
    crud.create_user(db, name, email, "password")
    return RedirectResponse("/users", status_code=303)


@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
def edit_user(request: Request, user_id: int, db: Session = Depends(get_db_sync)):
    user = crud.get_user(db, user_id)
    return templates.TemplateResponse("users/edit.html", {"request": request, "user": user})


@app.post("/users/update/{user_id}", response_class=HTMLResponse)
def update_user(user_id: int, db: Session = Depends(get_db_sync), name: str = Form(...), email: str = Form(...)):
    user = crud.get_user(db, user_id)
    if user:
        user.name = name
        user.email = email
        db.commit()
    return RedirectResponse("/users", status_code=303)


@app.post("/users/delete/{user_id}", response_class=HTMLResponse)
def delete_user(user_id: int, db: Session = Depends(get_db_sync)):
    crud.delete_user(db, user_id)
    return RedirectResponse("/", status_code=303)


@app.get("/posts", response_class=HTMLResponse)
def list_posts(request: Request, db: Session = Depends(get_db_sync)):
    posts = crud.get_all_posts(db)
    return templates.TemplateResponse("posts/list.html", {"request": request, "posts": posts})


@app.post("/posts/create", response_class=HTMLResponse)
def create_post(db: Session = Depends(get_db_sync), title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    crud.create_post(db, title, content, user_id)
    return RedirectResponse("/posts", status_code=303)


@app.get("/posts/edit/{post_id}", response_class=HTMLResponse)
def edit_post(request: Request, post_id: int, db: Session = Depends(get_db_sync)):
    post = crud.get_post(db, post_id)
    return templates.TemplateResponse("posts/edit.html", {"request": request, "post": post})


@app.post("/posts/update/{post_id}", response_class=HTMLResponse)
def update_post(post_id: int, db: Session = Depends(get_db_sync), title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    post = crud.get_post(db, post_id)
    if post:
        post.title = title
        post.content = content
        post.user_id = user_id
        db.commit()
    return RedirectResponse("/posts", status_code=303)


@app.post("/posts/delete/{post_id}", response_class=HTMLResponse)
def delete_post(post_id: int, db: Session = Depends(get_db_sync)):
    crud.delete_post(db, post_id)
    return RedirectResponse("/posts", status_code=303)
