from fastapi import FastAPI,Depends, status,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from schemas.users import UserPublic, UserCreate, UserPrivate, Token
from schemas.restaurants import RestaurantResponse, RestaurantCreate, RestaurantUpdate
from schemas.review import ReviewResponse, ReviewCreate
from typing import Annotated
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime, UTC, timedelta
import services.review as review_sv
import services.restaurant as restaurant_sv
import services.user as user_sv
from fastapi.security import OAuth2PasswordRequestForm
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():

    return f"<h1>Hello world</h1>"


@app.post("/api/v1/users", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate, db: Annotated[Session, Depends(get_db)],):
   return user_sv.create_user(user, db)

@app.post("/api/v1/auth/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: AsyncSession = Depends(get_db)):
    return await user_sv.login_for_access_token(form_data, db)



@app.get("/api/v1/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return user_sv.get_user(user_id, db)



@app.post("/api/v1/restaurants", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.create_restaurant(db, restaurant)
    

@app.get("/api/v1/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.get_restaurant(restaurant_id, db)

@app.get("/api/v1/restaurants", response_model=list[RestaurantResponse])
def get_all_restaurants_by_cuisine(cuisine: str, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.get_all_restaurants_by_cuisine(cuisine, db)
    

@app.delete("/api/v1/restaurants/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.delete_restaurant(restaurant_id, db)

@app.patch("/api/v1/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: int, restaurant: RestaurantUpdate, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.update_restaurant(restaurant_id, db, restaurant)

@app.post("/api/v1/restaurants/{restaurant_id}/reviews", response_model=ReviewResponse,  status_code=status.HTTP_201_CREATED)
def create_review(restaurant_id: int, review: ReviewCreate, db: Annotated[Session, Depends(get_db)],):
    return review_sv.create_review(db, restaurant_id, review)

@app.get("/api/v1/restaurants/{restaurant_id}/reviews", response_model=list[ReviewResponse])
def get_reviews_for_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
   return review_sv.get_reviews_for_restaurant(restaurant_id, db)

@app.delete("/api/v1/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Annotated[Session, Depends(get_db)],):
   return review_sv.delete_review(review_id, db)