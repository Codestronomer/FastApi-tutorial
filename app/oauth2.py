import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette import status
from .db import get_db
from . import schemas, models
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
SECRET_KEY = f"{settings.secret_key}"

# Algorithm
ALGORITHM = 'HS256'

# Expiration
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail='Could not validate credentials',
                                            headers={"WWW-Authenticate": "Bearer"})


    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user