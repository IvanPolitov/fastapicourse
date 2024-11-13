from pydantic import BaseModel
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
import jwt
import random
from datetime import timedelta, datetime, timezone

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = "dba749b064fa8502475b7bd8b31b81d2cb20a34fbfee762ba4ba9c09093c799a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


class User(BaseModel):
    username: str
    password: str


USER_DATA = [
    User(**{"username": "admin", "password": "admin"}),
    User(**{"username": "string", "password": "string"}),
]


def is_valid_user(user_in: User) -> User:
    print(user_in)
    for user in USER_DATA:
        if user.username == user_in.username and user.password == user_in.password:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials. Unauthorized."
    )


def get_jwt_from(data: User) -> str:
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        payload={
            "sub": data.username,
            "iat": now,
            # "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def imitate_data_acquiring(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        body = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=ALGORITHM
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your token has expired. Unauthorized."
        )
    return {"username": body["sub"], "sensitive_data": random.randint(1, 99)}


@app.post('/login')
async def login(data=Depends(is_valid_user)):
    print(type(data))
    token = get_jwt_from(data)
    return {'access_token': token, 'token_type': "bearer"}


@app.get('/protected_resource')
async def protected_resource(sensitive_data: dict = Depends(imitate_data_acquiring)):
    return sensitive_data
