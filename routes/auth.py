import logging
import os
from datetime import timedelta

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from services import auth_service

logger = logging.getLogger(__name__)

load_dotenv()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.verify_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"Tentativa de login falhou para o usuário: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = auth_service.create_access_token(
        data={"sub": user["id"]},
        expires_delta=access_token_expires
    )
    logger.info(f"Token criado com sucesso para o usuário: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        secret_key = os.getenv("SECRET_KEY")
        algorithm = os.getenv("ALGORITHM")

        if not secret_key or not algorithm:
            logger.error("Variáveis de ambiente 'SECRET_KEY' ou 'ALGORITHM' não estão configuradas corretamente.")
            raise credentials_exception

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("Token válido, mas sem o campo 'sub'.")
            raise credentials_exception
    except jwt.PyJWTError:
        logger.error(f"Erro ao decodificar o token: {str(e)}")
        raise credentials_exception
    return {"id": user_id}


@router.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    logger.info(f"Usuário {current_user.get('id')} acessou o endpoint /users/me")
    return current_user
