from fastapi import APIRouter,Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.views import auth
from app.schemas import LoginEmail

active_tokens = {}
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/",status_code=status.HTTP_200_OK)
def login(login:LoginEmail,db:Session = Depends(get_db)):
    support = auth.auth_user(login,db)
    active_tokens[f"tokens{login.email}"] = support["access_token"]

    return support