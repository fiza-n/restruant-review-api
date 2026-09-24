from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
import services.restaurant as restaurant_sv
from db.base import get_db
from schemas.restaurants import RestaurantResponse, RestaurantCreate, RestaurantUpdate
from core.dependencies import get_current_user
import models.users

router = APIRouter()

@router.post("", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.users.User, Depends(get_current_user)]
):
    return restaurant_sv.create_restaurant(db, restaurant, current_user)

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)]):
    return restaurant_sv.get_restaurant(db, restaurant_id)

@router.get("", response_model=list[RestaurantResponse])
def get_all_restaurants(
    db: Annotated[Session, Depends(get_db)],
    cuisine: str | None = None
):
    return restaurant_sv.get_all_restaurants_by_cuisine(db, cuisine)

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.users.User, Depends(get_current_user)]
):
    return restaurant_sv.delete_restaurant(db, restaurant_id, current_user)

@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant: RestaurantUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.users.User, Depends(get_current_user)]
):
    return restaurant_sv.update_restaurant( restaurant_id,db, restaurant, current_user)