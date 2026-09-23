from fastapi import APIRouter,Depends, status,HTTPException
import models.users
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy.orm import selectinload, Session
import services.user as user_sv
from db.base import get_db
from schemas.users import UserPublic,UserPrivate, Token
from services.auth import oauth2_scheme

router = APIRouter()

@router.get("/me", response_model=UserPrivate)
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)]):
    return user_sv.get_current_user(token, db)

@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return user_sv.get_user(user_id, db)


