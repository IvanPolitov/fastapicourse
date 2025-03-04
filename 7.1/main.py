from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()


class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    id: Optional[int] = None


users_db: dict[int, User] = {}


def id_generator():
    counter = 0
    if users_db:
        counter = max(users_db.keys())
    while True:
        counter += 1
        yield counter


id_gen = id_generator()


def check_user(user: User):
    errors = []
    for q in users_db.values():
        if user.username == q.username:
            errors.append(f"name={user.username} already taken")
        if user.email == q.email:
            errors.append(f"email={user.email} already taken")

    if errors:
        raise HTTPException(status_code=422, detail=", ".join(errors))


@app.post('/users', response_model=User, status_code=201)
def create_user(user: User):
    check_user(user)
    user.id = next(id_gen)
    users_db[user.id] = user
    return user


@app.get('/users/{id}', status_code=200, response_model=User)
def get_user(id: int):
    if id in users_db:
        return users_db[id]
    raise HTTPException(404, f"Contact with id={id} not found")


@app.delete('/users/{id}', status_code=204)
def delete_user(id: int):
    if id in users_db:
        del users_db[id]
        return
    raise HTTPException(404, f"Contact with id={id} not found")
