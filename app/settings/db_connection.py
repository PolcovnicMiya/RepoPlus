from dataclasses import dataclass
from app.settings.db_settings import settings
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
DB_PASS = settings.pg.DB_PASS
DB_HOST = settings.pg.DB_HOST
DB_NAME = settings.pg.DB_NAME
DB_USER = settings.pg.DB_USER
DB_PORT = settings.pg.DB_PORT
print(settings.pg.DB_NAME)
@dataclass
class DataBaseConnection:
    url : str  = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo : bool = True
    echo_pool : bool = False
    pool_size : int = 5
    max_overflow : int = 10

    def __init__(self):
        self.async_engine = create_async_engine(
            url = self.url,
            echo = self.echo,
            echo_pool = self.echo_pool,
            pool_size = self.pool_size,
            max_overflow = self.max_overflow,
            )
        self.session_factory = async_sessionmaker(
            bind = self.async_engine,
            autoflush = False,
            autocommit = False,
            expire_on_commit = False,
        )

    async def dispoce(self):
        await self.async_engine.dispose()   

    async def session_use(self):
        async with self.session_factory() as session:
            yield session

db_session = DataBaseConnection()
engine = create_async_engine(url = db_session.url)