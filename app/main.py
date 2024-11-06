from fastapi import FastAPI
from fastapi.responses import FileResponse
from models.models import User, Feedback

app = FastAPI()
user = User(name='John Doe', id=1, age=18)

fake_users = {
    1: {'username': 'johndoe', 'email': 'johndoe@example.com'},
    2: {'username': 'janedoe', 'email': 'janedoe@example.com'},
    3: {'username': 'jane', 'email': 'jane@example.com'},
    4: {'username': 'jane', 'email': 'jane@example.com'},

}


def make_message(name):
    return f"Feedback received. Thank you, {name}!"


@app.post('/feedback')
async def ffeedback(feedback: Feedback):
    message = make_message(feedback.name)
    return {"message": message}


@app.get('/users/{user_id}')
async def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    else:
        return {"error": "User not found"}
