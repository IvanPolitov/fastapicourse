from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.todo import ToDoFromDB, ToDoCreate
from app.db.database import get_async_session
from app.repositories.todo_repository import ToDoRepository, SqlAlchemyToDoRepository

todo_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"]
)


# тут нам нужна функция по инициализации ТуДу-репозитория (для уменьшения количества кода)
async def get_todo_repository(session: AsyncSession = Depends(get_async_session)) -> ToDoRepository:
    return SqlAlchemyToDoRepository(session)


# наши роуты стали значительно короче
@todo_router.get("/", response_model=list[ToDoFromDB])
async def get_todos(repo: ToDoRepository = Depends(get_todo_repository)):
    return await repo.get_todos()


# можно заметить, что оба роута зависят от общей функции получения репозитория,
# которая зависит от сессий -> это пример цепочки инъекции зависимостей
@todo_router.post("/", response_model=ToDoFromDB)
async def create_todo(todo: ToDoCreate, repo: ToDoRepository = Depends(get_todo_repository)):
    return await repo.create_todo(todo)
