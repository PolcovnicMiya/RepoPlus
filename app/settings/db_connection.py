from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db_settings import settings

DB_PASS = settings.pg.DB_PASS
DB_HOST = settings.pg.DB_HOST
DB_NAME = settings.pg.DB_NAME
DB_USER = settings.pg.DB_USER
DB_PORT = settings.pg.DB_PORT

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine ( url = DB_URL , 

)