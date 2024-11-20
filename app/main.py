from functools import wraps
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt


class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'guest'


USER_DATA = [
    {'username': 'admin', 'password': 'admin', 'role': 'admin_role'},
    {'username': 'user', 'password': 'user', 'role': 'admin_role'},
    {'username': 'guest', 'password': 'guest', 'role': 'guest_role'},
]

SECRET_KEY = 'secret'
ALGORITHM = 'HS256'
EXPIRES_IN = 100

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


def create_access_token(user: dict) -> str:
    payload = {
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.now(timezone.utc) + timedelta(minutes=EXPIRES_IN),
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def role_access(role: str):
    def wrapped(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            payload = jwt.decode(kwargs['token'], SECRET_KEY, ALGORITHM)

            for user in USER_DATA:
                if payload['username'] == user['username']:
                    if user['role'] == role:
                        return func(*args, **kwargs)
            raise HTTPException(status_code=401, detail="Invalid token", headers={
                "WWW-Authenticate": "Bearer"})
        return wrap
    return wrapped


@app.post('/login')
async def login(input_user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_from_db(input_user)
    token = create_access_token(user)
    return {'message': 'You are logged in', 'access_token': token, "token_type": "bearer"}


@app.post('/protected')
@role_access('admin_role')
def protected(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={
                            "WWW-Authenticate": "Bearer"})
    current_user = None
    for user in USER_DATA:
        if payload['username'] == user['username']:
            current_user = user
    return {'message': f'Hello, {current_user['username']}', 'role': current_user['role']}


@app.get('/')
async def root(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={
                            "WWW-Authenticate": "Bearer"})
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={
                            "WWW-Authenticate": "Bearer"})
    return {'message': 'Hello World'}

if __name__ == '__main__':
    pass
