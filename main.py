import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app import router as all_router
from app.settings.db_connection import db_session
from app.settings.logging import log_conf
from app.helper.tables import create_tables, delete_tables, create_tables_test

log = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    log_conf(level=logging.INFO)
    log.debug(db_session.url)
    log.info("Успешный запуск")
    await create_tables()
    await create_tables_test()
    yield
    # finish
    log.info("приложение выключилось")
    # await delete_tables()
    await db_session.dispoce()


app = FastAPI(
    lifespan=lifespan,
    debug=True,
    title = "BaseConfig",
    summary="It my Base project for use in future project",
    description= """  ChimichangApp API helps you do awesome stuff.

                                ## Users

                                You will be able to:

                                CRUD

                                """
)

app.include_router(all_router)


@app.get("/")
def standart():
    return {"hello": "епт"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
