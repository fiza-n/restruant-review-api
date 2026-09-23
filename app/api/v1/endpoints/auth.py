from fastapi import APIRouter,Depends, status,HTTPException
import models.users
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import selectinload, Session
import services.user as user_sv
from db.base import get_db
from schemas.users import UserPublic, UserCreate, UserPrivate, Token


router = APIRouter()

@router.post("/register", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate, db: Annotated[Session, Depends(get_db)],):
   return user_sv.create_user(user, db)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Annotated[AsyncSession, Depends(get_db)]):
    return user_sv.login_for_access_token(form_data, db)

