from fastapi import FastAPI
import uvicorn
from app import router as all_router
from contextlib import asynccontextmanager
from app.settings.db_connection import db_session
import logging
from app.settings.logging import log_conf

log = logging.getLogger("__name__")

@asynccontextmanager
async def lifespan(app:FastAPI):
    log_conf()
    log.info("Успешный запуск")
    #start
    yield
    #finish
    log.info("приложение выключилось")
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