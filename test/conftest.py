import asyncio
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from app.helper.tables import create_tables_test,delete_tables_test
from main import app



@pytest_asyncio.fixture(scope='session')
async def prepare_database():
    create_tables_test()
    yield
    delete_tables_test()

# SETUP
@pytest_asyncio.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case.""" 
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac