from pydantic import BaseModel, EmailStr, PositiveInt


class User(BaseModel):
    username: str
    password: str
