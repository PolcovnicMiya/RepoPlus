from abc import ABC, abstractmethod
import logging

from sqlalchemy import insert, delete, select, update, text
from app.settings.db_connection import db_session


log = logging.getLogger()


class AbstractRepo(ABC):
    @abstractmethod
    async def get_one(self, filters):
        raise NotImplementedError

    async def get_all(self, filters):
        raise NotImplementedError

    async def add_one(self, data):
        raise NotImplementedError

    async def delete_one(self, id):
        raise NotImplementedError

    async def edit_one(self, data, filters):
        raise NotImplementedError

    async def edit_some(self, data, filters):
        raise NotImplementedError


class SQLAlchemyRepo(AbstractRepo):
    model = None

    async def get_one(self, **filters):
        async with db_session.session_factory() as session:
            stmt = select(self.model).filter_by(**filters)
            result = await session.execute(stmt)
            final = result.scalar_one_or_none()
            if final is not None:
                return final

    async def get_all(self, **filters):
        async with db_session.session_factory() as session:
            stmt = select(self.model)
            if filters:
                log.info(filters)
                filters = filters.get("filters")
                stmt = stmt.filter_by(**filters)
            result = await session.execute(stmt)
            final = [row[0].to_read_model() for row in result.all()]
            return final

    async def add_one(self, data: dict):
        async with db_session.session_factory() as session:
            stmt = insert(self.model).values(data).returning(self.model.id)
            result = await session.execute(stmt)
            await session.commit()
            final = result.scalar_one_or_none()
            if final is not None:
                return final

    async def edit_one(self, data, **filters):
        async with db_session.session_factory() as session:
            log.debug(data)
            log.debug(filters)
            stmt = (
                update(self.model)
                .filter_by(**filters)
                .values(data)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()

    async def edit_some(self, data, **filters):
        async with db_session.session_factory() as session:
            log.debug(filters)
            log.debug(data)
            stmt = (
                update(self.model)
                .filter_by(**filters)
                .values(data)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            final = [row[0].to_read_model() for row in result.all()]
            return final

    async def delete_one(self, **filters):
        async with db_session.session_factory() as session:
            log.debug(filters)
            stmt = delete(self.model).filter_by(**filters)
            result = await session.execute(stmt)
            await session.commit()
            return bool(result.rowcount)


class RedisAbstractRepo(ABC):
    @abstractmethod
    async def set_value(self, keys, value, exp):
        NotImplementedError

    @abstractmethod
    async def get_value(self, keys):
        NotImplementedError

    @abstractmethod
    async def delete_value(self, keys):
        NotImplementedError


class RedisRepo(RedisAbstractRepo):
    def __init__(self):
        self._redis = redis()

    async def set_value(self, keys, value, exp):
        result = await self._redis.set(
            name=keys,
            value=value,
        )

    async def get_value(self, keys):
        result = await self._redis.get(name=keys)

    async def delete_value(self, keys):
        result = await self._redis.delete(name=keys)
