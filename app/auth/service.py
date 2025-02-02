from sqlalchemy.orm import Session
from ..users.models import User
from ..core.security import get_password_hash, verify_password
from ..config.jwt import create_access_token
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    def register(db: Session, email: str, password: str):
        # Verificar si el usuario ya existe
        if AuthService.check_email_exists(db, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Crear nuevo usuario
        hashed_password = get_password_hash(password)
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @staticmethod
    def create_token(email: str):
        return {
            "access_token": create_access_token({"sub": email}),
            "token_type": "bearer"
        }

    @staticmethod
    def check_email_exists(db: Session, email: str) -> bool:
        user = db.query(User).filter(User.email == email).first()
        return user is not None