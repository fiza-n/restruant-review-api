from fastapi import FastAPI,Depends, status,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.schemas.users import UserResponse, UserCreate
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

import models.restaurants, models.reviews, models.users
from db.base import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")
users = []

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():

    return f"<h1>Hello world</h1>"


@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.users.User).where(models.users.User.username == user.username),)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    new_user = {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    users.append(new_user)
    return new_user

