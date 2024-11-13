from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt


class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'guest'


USER_DATA = [
    {'username': 'admin', 'password': 'admin'},
    {'username': 'user', 'password': 'user'},
    {'username': 'guest', 'password': 'guest'},
]

SECRET_KEY = 'secret'
ALGORITHM = 'HS256'
EXPIRES_IN = 1

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def get_user_from_db(input_user: User):
    for user in USER_DATA:
        if input_user.username == user['username'] and input_user.password == user['password']:
            return user
    raise HTTPException(
        status_code=401,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'}
    )


def create_access_token(user: User) -> str:
    payload = {
        'username': user.username,
        'role': user.role,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=EXPIRES_IN),
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post('/login')
async def login(input_user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_from_db(input_user)
    token = create_access_token(User(**user))
    return {'message': 'You are logged in', 'token': token}
