from fastapi import Depends, FastAPI, Request, HTTPException, Response
from pydantic import BaseModel
from fastapi.security import HTTPBasicCredentials, HTTPBasic


app = FastAPI()
security = HTTPBasic()


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


def authenticate_user(creds: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(creds.username)
    if user and user.password == creds.password:
        return user

    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get('/login')
def protected(user: User = Depends(authenticate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}



