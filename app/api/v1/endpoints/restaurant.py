from fastapi import APIRouter,Depends, status,HTTPException
import models.users
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy.orm import selectinload, Session
import services.restaurant as restaurant_sv
from db.base import get_db
from schemas.restaurants import RestaurantResponse, RestaurantCreate, RestaurantUpdate
from services.auth import oauth2_scheme

router = APIRouter()

@router.post("", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.create_restaurant(db, restaurant)

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.get_restaurant(restaurant_id, db)

@router.get("", response_model=list[RestaurantResponse])
def get_all_restaurants_by_cuisine(cuisine: str, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.get_all_restaurants_by_cuisine(cuisine, db)

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.delete_restaurant(restaurant_id, db)

@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: int, restaurant: RestaurantUpdate, db: Annotated[Session, Depends(get_db)],):
    return restaurant_sv.update_restaurant(restaurant_id, db, restaurant)