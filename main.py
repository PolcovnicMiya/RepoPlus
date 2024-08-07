from fastapi import FastAPI
import uvicorn
from app import router as all_router
from contextlib import asynccontextmanager
from app.settings.db_connection import db_session


@asynccontextmanager
async def lifespan(app:FastAPI):
    #start
    yield
    #finish
    await db_session.dispoce()


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(all_router)

@app.get("/")
def standart():
    return{
        "hello":"епт"
    }

if __name__ == "__main__":
    uvicorn.run(app = "main:app")