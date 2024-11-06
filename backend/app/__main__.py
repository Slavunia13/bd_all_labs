import os
import sys
from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

sys.path.append(os.path.join(os.getcwd(), os.pardir, os.pardir))

from app.config import DefaultSettings
from app.config.utils import getSettings
from app.endpoints import listOfRoutes

from app.db.connection import redis_manager
from app.db.connection import mongo_manager
from app.db.connection import neo4j_manager

logger = getLogger(__name__)


def bindRoutes(application: FastAPI, setting: DefaultSettings) -> None:
    for route in listOfRoutes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def getApp() -> FastAPI:
    description = "Выполнил Кирпиченко В.Л., группа 22305, 02.11.2024"

    tags_metadata = [
        {
            "name": "Health check",
        },
        {
            "name": "Lab1",
        },
        {
            "name": "Lab2",
        },
        {
            "name": "Lab3",
        },
        {
            "name": "Lab4",
        },
        {
            "name": "Lab5",
        },
        {
            "name": "Lab6",
        }
    ]

    application = FastAPI(
        title="Лабы по БД, 5 сем.",
        docs_url="/swagger",
        openapi_url="/openapi",
        description=description,
        version="1.0.0",
        openapi_tags=tags_metadata,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    settings = getSettings()
    bindRoutes(application, settings)
    application.state.settings = settings
    return application


app = getApp()

# Подключение к Redis при старте приложения
@app.on_event("startup")
async def startup_event():
    await redis_manager.connect()
    await mongo_manager.connect()
    await neo4j_manager.connect()

# Отключение от Redis при завершении приложения
@app.on_event("shutdown")
async def shutdown_event():
    await redis_manager.disconnect()
    await mongo_manager.disconnect()
    await neo4j_manager.disconnect()


if __name__ == "__main__":  # pragma: no cover
    settings_for_application = getSettings()
    run(
        "__main__:app",
        port=settings_for_application.BACKEND_PORT,
        reload=True,
        reload_dirs=["app", "tests"],
        log_level="debug",
        host=settings_for_application.BACKEND_HOST,
    )
