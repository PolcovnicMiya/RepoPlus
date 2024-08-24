from abc import ABC, abstractmethod
import logging
from sqlalchemy import insert, delete, select, update
from app.settings.db_connection import db_session


log = logging.getLogger()


class AbstracrRepo(ABC):
    @abstractmethod
    async def get_one(self, filter):
        raise NotImplementedError

    async def get_all(self, filter):
        raise NotImplementedError

    async def add_one(self, body):
        raise NotImplementedError

    async def delete_one(self, id):
        raise NotImplementedError

    async def delete_some(self, filter):
        raise NotImplementedError

    async def edit_one(self, id):
        raise NotImplementedError


class SQLAlchemyRepo(AbstracrRepo):
    model = None

    async def get_one(self, **filter):
        async with db_session.session_factory() as session:
            stmt = select(self.model).filter_by(**filter)
            result = await session.execute(stmt)
            final = result.scalar_one_or_none()
            if final is not None:
                return final

    async def get_all(self, **filters):
        async with db_session.session_factory() as session:
            stmt = select(self.model)
            if filters:
                log.degug("Сработалая")
                stmt = stmt.filter_by(**filters)
            result = await session.execute(stmt)
            final = [row[0].to_read_model() for row in result.all()]
            return final

    async def add_one(self, body: dict):
        async with db_session.session_factory() as session:
            stmt = insert(self.model).values(body).returning(self.model.id)
            result = await session.execute(stmt)
            await session.commit()
            final = result.scalar_one_or_none()
            if final is not None:
                return final
