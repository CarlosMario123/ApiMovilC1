from datetime import datetime, timedelta
import jwt

SECRET_KEY = "api"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 52560000  

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)