from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException,status
from datetime import datetime, timedelta
from app.hashing import Hash
from app.token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES

def auth_user(user, db: Session):
    user_db = db.query(models.User).filter(models.User.email == user.email).first()
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el email: {user.email}"
        )
    if not Hash.verify_password(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password incorrect"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "email" : user.email,
    }