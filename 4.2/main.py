from typing import Annotated
from fastapi import Depends, FastAPI, Request, HTTPException, Response
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
import jwt

app = FastAPI()


ALGORITHM = "HS256"
SECRET_KEY = "mysecretkey"
oauth_scheme = OAuth2PasswordBearer(tokenUrl='login/')


class User(BaseModel):
    username: str
    password: str


USER_DATA = [User(**{"username": "user1", "password": "pass1"}),
             User(**{"username": "user2", "password": "pass2"})]


# симуляционный пример
def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


def generate_jwt_token(data):
    return jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)


@app.post('/login')
def login(credetials: User):
    user = get_user_from_db(credetials.username)
    if user:
        if user.password == credetials.password:
            return {'access_token': generate_jwt_token({'sub': user.username}), 'token_type': 'bearer'}

    return HTTPException(401, 'Invalid credentials')


def exists_user_from_token(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        if payload.get('sub'):
            return {'message': 'Успешный вход'}
    except jwt.ExpiredSignatureError:
        return HTTPException(status_code=401, detail='Истекло время жизни токена')
    except jwt.InvalidTokenError:
        return HTTPException(status_code=401, detail='Неправильный токен')
    finally:
        return HTTPException(status_code=401, detail='Ошибка авторизации')


@app.get('/protected')
def protected(result: dict = Depends(exists_user_from_token)):
    if result:
        return {'message': 'Access'}
    return {'message': 'Not access'}
