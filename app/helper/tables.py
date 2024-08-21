import logging
from app.settings.db_connection import db_session
from app.model import Base
from app.settings.db_connection import engine
log = logging.getLogger("__name__")


async def create_tables():
    async with db_session.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        log.debug("функция создания таблиц")


async def delete_tables():
    async with db_session.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        log.debug("функция удаления таблиц")

