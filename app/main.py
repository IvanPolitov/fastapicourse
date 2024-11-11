from fastapi import FastAPI, Cookie, Response
from models.models import User
from random import randint

app = FastAPI()
sample = [
    {'username': 'admin', 'password': 'admin'},
    {'username': 'user', 'password': 'user'},
]

dbusers = [User(**q) for q in sample]

sessions = {}


@app.post('/login')
async def login(user: User, response: Response):
    for person in dbusers:
        if user.username == person.username and user.password == person.password:
            session_token = str(randint(0, 1000))
            sessions[session_token] = user
            response.set_cookie(key='session_token',
                                value=session_token, httponly=True)
            print(sessions)
            return {'message': 'Cookie ready'}
    return {'message': 'Invalid credentials'}


@app.get('/user')
async def get_user(session_token=Cookie()):
    print(sessions)
    print(session_token)

    user = sessions.get((session_token))
    if user:
        return user.dict()
    return {'message': 'Invalid credentials'}
