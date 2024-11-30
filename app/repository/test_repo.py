from abc import ABC, abstractmethod
import logging
from sqlalchemy import insert, delete, select, update, text
from app.settings.db_connection import db_session
from app.repository.repo import AbstractRepo

log = logging.getLogger()


class SQLAlchemyRepoPlus(AbstractRepo):
    model = None

    async def _get_one(self, session_local, **filters):
        async with session_local as session:
            stmt = select(self.model).filter_by(**filters)
            result = await session.execute(stmt)
            final = result.scalar_one_or_none()
            if final is not None:
                return final

    async def get_one(self, test=False, **filters):
        if test:
            session_local = db_session.test_session_factory()
        else:
            session_local = db_session.session_factory()
        return await self._get_one(session_local=session_local, **filters)

    async def _get_all (self, session_local, **filters):
        async with session_local as session:
            stmt = select(self.model)
            if filters:
                log.info(filters)
                filters = filters.get("filters")
                stmt = stmt.filter_by(**filters)
            result = await session.execute(stmt)
            final = [row[0].to_read_model() for row in result.all()]
            return final
            
    async def get_all(self, test=False, **filters):
        if test:
            session_local = db_session.test_session_factory()
        else:
            session_local = db_session.session_factory()
        return await self._get_all(session_local=session_local, **filters)

    async def _add_one(self, session_local, **data: dict):
        async with session_local as session:
            stmt = insert(self.model).values(data).returning(self.model.id)
            result = await session.execute(stmt)
            await session.commit()
            final = result.scalar_one_or_none()
            if final is not None:
                return final
            
    async def add_one(self, data: dict, test=False):
        if test:
            session_local = db_session.test_session_factory()
        else:
            session_local = db_session.session_factory()
        return await self._add_one(session_local=session_local, **data)
    

    async def _edit_one(self, session_local, data, **filters):
        async with session_local as session:
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
        
    async def edit_one(self, data, test : bool =False, **filters):
        if test:
            session_local = db_session.test_session_factory()
        else:
            session_local = db_session.session_factory()
        return await self._edit_one(session_local=session_local, data = data, **filters)

    async def _edit_some(self, session_local, data, **filters):
        async with session_local as session:
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

    async def edit_some(self, data, test=False, **filters):
        if test:
            session_local = db_session.test_session_factory()
        else:
            session_local = db_session.session_factory()
        return await self._edit_some(session_local=session_local,data=data, **filters)


    async def _delete_one(self,session_local, **filters):
        async with session_local as session:
            log.debug(filters)
            stmt = delete(self.model).filter_by(**filters)
            result = await session.execute(stmt)
            await session.commit()
            return bool(result.rowcount)

    async def delete_one(self, test=False, **filters):
        if test:
            session_local = db_session.test_session_factory()
        else:
            session_local = db_session.session_factory()
        return await self._delete_one(session_local=session_local, **filters)


