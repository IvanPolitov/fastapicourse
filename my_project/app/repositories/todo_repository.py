from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.todo import ToDoCreate
from app.db.models import ToDo


class ToDoRepository(ABC):  # это абстрактный интерфейс нашего репозитория
    @abstractmethod
    async def get_todos(self) -> list[ToDo]:
        pass

    @abstractmethod
    async def create_todo(self, todo: ToDoCreate) -> ToDo:
        pass


# это его конкретное исполнение для алхимии (можно сделать для peewee, pony и тд, легко поменять способ реализации)
class SqlAlchemyToDoRepository(ToDoRepository):
    # при инициализации принимает асинхронную сессию
    def __init__(self, session: AsyncSession):
        self.session = session

    # далее, по сути, код из эндпоинтов с предыдущего шага
    async def get_todos(self) -> list[ToDo]:
        result = await self.session.execute(select(ToDo))
        return result.scalars().all()

    async def create_todo(self, todo: ToDoCreate) -> ToDo:
        new_todo = ToDo(**todo.model_dump())
        self.session.add(new_todo)
        await self.session.commit()
        await self.session.refresh(new_todo)
        return new_todo
