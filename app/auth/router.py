from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..config.database import get_db
from .schemas import UserAuth, Token, EmailCheck
from .service import AuthService

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user_data: UserAuth, db: Session = Depends(get_db)):
    user = AuthService.register(db, user_data.email, user_data.password)
    return AuthService.create_token(user.email)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = AuthService.authenticate(db, form_data.username, form_data.password)
    return AuthService.create_token(user.email)

@router.get("/check-email/{email}")
async def check_email(email: str, db: Session = Depends(get_db)):
    exists = AuthService.check_email_exists(db, email)
    return {
        "email": email,
        "exists": exists,
        "message": "Email already registered" if exists else "Email available"
    }