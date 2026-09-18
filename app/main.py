from fastapi import FastAPI,Depends, status,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from schemas.users import UserResponse, UserCreate
from schemas.restaurants import RestaurantResponse, RestaurantCreate, RestaurantUpdate
from schemas.review import ReviewResponse, ReviewCreate
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, UTC
analyzer = SentimentIntensityAnalyzer()


import models.restaurants, models.reviews, models.users
from db.base import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():

    return f"<h1>Hello world</h1>"


@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.users.User).where(models.users.User.username == user.username),)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    result = db.execute(select(models.users.User).where(models.users.User.email == user.email),)
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user = models.users.User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.users.User).where(models.users.User.id == user_id),)

    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")



@app.post("/api/v1/restaurants", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate, db: Annotated[Session, Depends(get_db)],):
    result = db.execute(
        select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.title == restaurant.title)
    )
    existing_restaurant = result.scalars().first()
    if existing_restaurant:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Restaurant already exists")

    new_restaurant = models.restaurants.Restaurants(
        title=restaurant.title,
        location=restaurant.location,
        cuisine=restaurant.cuisine,
        contact_number=restaurant.contact_number,
        owner_id=1
        

    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

@app.get("/api/v1/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.id == restaurant_id))

    existing_restaurant = result.scalars().first()
    if existing_restaurant:
        return existing_restaurant
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

@app.get("/api/v1/restaurants", response_model=list[RestaurantResponse])
def get_all_restaurants_by_cuisine(cuisine: str, db: Annotated[Session, Depends(get_db)],):
    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.cuisine == cuisine))
    restaurants = result.scalars().all()
    if restaurants:
        return restaurants
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No restaurants found for the specified cuisine")

@app.delete("/api/v1/restaurants/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.id == restaurant_id))
    existing_restaurant = result.scalars().first()
    if not existing_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    db.delete(existing_restaurant)
    db.commit()
    return 

@app.patch("/api/v1/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: int, restaurant: RestaurantUpdate, db: Annotated[Session, Depends(get_db)],):
    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.id == restaurant_id))
    existing_restaurant = result.scalars().first()
    if not existing_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    existing_restaurant.title = restaurant.title
    existing_restaurant.location = restaurant.location
    existing_restaurant.cuisine = restaurant.cuisine
    existing_restaurant.contact_number = restaurant.contact_number

    db.commit()
    db.refresh(existing_restaurant)
    return existing_restaurant
@app.post("/api/v1/restaurants/{restaurant_id}/reviews", response_model=ReviewResponse,  status_code=status.HTTP_201_CREATED)
def create_review(restaurant_id: int, review: ReviewCreate, db: Annotated[Session, Depends(get_db)],):

    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.id == restaurant_id))
    existing_restaurant = result.scalars().first()
    if not existing_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")


    scores = analyzer.polarity_scores(review.body)
    compound = scores["compound"]
    
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    
    new_review = models.reviews.Reviews(
                title=review.title,
                body=review.body,
                rating=review.rating,
                sentiment_label=label,
                sentiment_score=compound,
                user_id=1,
                restaurants_id=restaurant_id,
                review_posted=datetime.now(UTC)
    
            )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

    all_reviews = db.execute(select(models.reviews.Reviews).where(
        models.reviews.Reviews.restaurant_id == restaurant_id
    ))
    reviews_list = all_reviews.scalars().all()
    existing_restaurant.avg_rating = sum(r.rating for r in reviews_list) / len(reviews_list)
    db.commit()

    return new_review

@app.get("/api/v1/restaurants/{restaurant_id}/reviews", response_model=list[ReviewResponse])
def get_reviews_for_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
    result = db.execute(select(models.reviews.Reviews).where(models.reviews.Reviews.restaurants_id == restaurant_id))
    reviews = result.scalars().all()
    if reviews:
        return reviews
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found for the specified restaurant")

@app.delete("/api/v1/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Annotated[Session, Depends(get_db)],):
    result = db.execute(select(models.reviews.Reviews).where(models.reviews.Reviews.id == review_id))
    existing_review = result.scalars().first()
    if not existing_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    db.delete(existing_review)
    db.commit()
    return