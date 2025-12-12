import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app import router as all_router
from app.settings.db_connection import db_session
from app.settings.loggi import log_conf
from app.helper.tables import create_tables, delete_tables, create_tables_test
import os


log = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    log_conf(level=logging.ERROR)
    log.debug(db_session.url)
    log.info("Успешный запуск")
    await create_tables()
    # await create_tables_test()
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


os.makedirs("media/products", exist_ok=True)


app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(all_router)


@app.get("/")
def standart():
    return {"hello": "IITU"}

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        workers=1
    )
