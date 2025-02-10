import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from dotenv import load_dotenv

load_dotenv()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


def verify_user(username: str, password: str) -> Optional[dict]:
    if username == "admin" and password == "admin":
        return {"id": "123", "username": username}
    return None
