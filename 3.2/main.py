from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    username: str
    password: str


db = [User(**{'username': '1', 'password': '123'})]


@app.post('/login')
async def login(user: User, response: Response):
    for db_user in db:
        if user.username == db_user.username and user.password == db_user.password:
            session_token = 'qqqq'
            response.set_cookie(key='session_token',
                                value=session_token, httponly=True)
            return user
    return {'message': "nonono"}


@app.get('/unlogin')
async def unlogin(response: Response):
    response.delete_cookie(key='session_token')
    return {'message': "delete_cookie"}


@app.get('/user')
async def user(request: Request):
    session_token = request.cookies.get('session_token', None)
    if session_token:
        return User(**{"username": "1", "password": "123"})
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
