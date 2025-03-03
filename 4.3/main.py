from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt


class User(BaseModel):
    username: str
    password: str
    role: str | None


ALGORITHM = "HS256"
SECRET_KEY = "mysecretkey"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

USER_DATA = [User(**{"username": "user1", "password": "pass1", 'role': 'admin'}),
             User(**{"username": "user2", "password": "pass2", 'role': 'guest'})]


app = FastAPI()


def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


def generate_jwt_token(data):
    return jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)


def exists_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        a = payload.get('sub')
        if payload.get('sub'):
            return {'message': 'Успешный вход', 'role': a}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail='Истекло время жизни токена')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Неправильный токен')
    except Exception:
        raise HTTPException(status_code=401, detail='Ошибка авторизации')


@app.post('/login')
def login(credentials: User = Depends(OAuth2PasswordRequestForm)):
    user = get_user_from_db(credentials.username)
    if user:
        if user.password == credentials.password:
            return {'access_token': generate_jwt_token({'sub': user.role}), 'token_type': 'bearer'}

    return HTTPException(401, 'Invalid credentials')


@app.get("/protected")
def protected(result: dict = Depends(exists_user_from_token)):
    if result.get('role') == 'admin':
        return {'message': 'Access'}
    return {'message': 'Not access'}
