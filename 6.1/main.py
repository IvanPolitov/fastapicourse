from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
app = FastAPI()


class User(BaseModel):
    username: str
    password: str
    role: str | None

# ДОБАВИЛИ модель пидантика для ошибок


class CustomExceptionModel(BaseModel):
    status_code: int
    er_message: str
    er_details: str


class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


@app.exception_handler(CustomExceptionA)
async def custom_exception_handler(request: Request, exc: CustomExceptionA):
    error = jsonable_encoder(CustomExceptionModel(
        status_code=exc.status_code, er_message='asdasdasd', er_details=exc.detail))
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(CustomExceptionB)
async def custom_exception_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": 'qweqweqweqweqw'}
    )

ALGORITHM = "HS256"
SECRET_KEY = "mysecretkey"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

USER_DATA = [User(**{"username": "user1", "password": "pass1", 'role': 'admin'}),
             User(**{"username": "user2", "password": "pass2", 'role': 'guest'})]


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
    raise CustomExceptionA(detail="Item not found", status_code=404)


@app.get("/protectedqq")
def protectedqq(result: dict = Depends(exists_user_from_token)):
    if result.get('role') == 'guest':
        return {'message': 'Access'}
    raise CustomExceptionB(detail="Item not found", status_code=404)
