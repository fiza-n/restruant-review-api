from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from db.base import get_db
from services.auth import oauth2_scheme, verify_access_token
import models.users
from sqlalchemy import select

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    user_id = verify_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = db.execute(
        select(models.users.User).where(models.users.User.id == int(user_id))
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user