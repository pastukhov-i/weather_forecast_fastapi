from fastapi import FastAPI

from src.config.logging import init_logger
from src.container import RootContainer
from src.forecast.router import forecast_router


def create_app() -> FastAPI:
    init_logger()
    RootContainer()

    app = FastAPI()

    app.include_router(forecast_router)

    return app


app = create_app()
