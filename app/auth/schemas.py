# app/auth/schemas.py
from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EmailCheck(BaseModel):
    email: EmailStr
    exists: bool
    message: str