from fastapi import FastAPI, Depends, HTTPException, status
from models.models import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

USER_DATA = [
    User(**{'username': 'user1', 'password': 'password1'}),
    User(**{'username': 'user2', 'password': 'password2'}),
    User(**{'username': 'user3', 'password': 'password3'}),
]


def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or credentials.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Autheticate': 'Basic'}
        )
    return user


@app.get('/protected_resource')
async def get_resource(user: User = Depends(authenticate_user)):
    return {'message': 'You got my secret, welcome', 'user': user}


@app.get("/logout")
def logout():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You have successfully logged out",
        headers={"WWW-Authenticate": "Basic"},
    )
