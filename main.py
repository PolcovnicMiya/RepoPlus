from fastapi import FastAPI
import uvicorn
import logging
from contextlib import asynccontextmanager
from app import router as all_router
from app.settings.db_connection import db_session
from app.settings.logging import log_conf
from app.helper.tables import create_tables, delete_tables
log = logging.getLogger("__name__")




@asynccontextmanager
async def lifespan(app:FastAPI):
    #start
    log_conf(level=logging.INFO)
    log.debug(db_session.url)
    log.info("Успешный запуск")
    await create_tables()
    yield
    #finish
    log.info("приложение выключилось")
    await delete_tables()
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