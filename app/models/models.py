from pydantic import BaseModel, EmailStr, PositiveInt


class UserCreate(BaseModel):
    id: PositiveInt
    name: str
    is_subscribed: bool | None = None
    age: PositiveInt
    email: EmailStr


class Feedback(BaseModel):
    name: str
    message: str


class Product(BaseModel):
    product_id: PositiveInt
    name: str | None
    category: str | None
    price: float
