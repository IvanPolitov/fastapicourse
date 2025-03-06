import datetime

from pydantic import BaseModel


class ToDoCreate(BaseModel):
    description: str
    completed: bool | None = False


# будем возвращать из БД - унаследовались от создания и расширили 2 полями
class ToDoFromDB(ToDoCreate):
    id: int
