from fastapi import FastAPI
from fastapi.responses import FileResponse
from models.models import User

app = FastAPI()
user = User(name='John Doe', id=1, age=18)


def is_adult(user):
    return user.age >= 18


@app.get('/users')
async def root():
    return user


@app.post('/user')
async def check_user(user: User):
    return {"is_adult": 'Yes' if is_adult(user) else 'No'}
