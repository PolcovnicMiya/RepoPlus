import pytest
import asyncio
from httpx import ASGITransport, AsyncClient
from main import app as application

@pytest.mark.asyncio
async def test_standart():
    async with AsyncClient(transport=ASGITransport(app=application),base_url="http://testserver") as ac:
        responce = await ac.get("/")
    assert responce.status_code == 200
    assert responce.json() == {"hello": "епт"}

@pytest.mark.asyncio
async def test_create(prepare_database,ac: AsyncClient):
    response =await ac.post("/v2/users/create",
        params={
            "test" : "true" 
        }, 
        json={
            "username": "string",
            "password": "string",
            "email": "user@example.com",
            "in_match": "true"
        }
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_user(ac: AsyncClient):
    response =await ac.get("/v2/users/",    
    params={"user_id" : "1",
            "test" : "true" }
    )
    assert response.status_code == 200
    assert response.json() != { 'result' : None }


    