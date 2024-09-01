import pytest
from httpx import ASGITransport, AsyncClient
from main import app as application

@pytest.mark.anyio
async def test_standart():
    async with AsyncClient(transport=ASGITransport(app=application),base_url="http://test") as ac:
        responce = await ac.get("/")
    assert responce.status_code == 200
    assert responce.json() == {"hello": "епт"}

    
