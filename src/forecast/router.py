from typing import Annotated

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from src.forecast.container import ForecastContainer
from src.forecast.schemas import CurrentForecastSchema
from src.forecast.schemas import ForecastCreateSchema
from src.forecast.schemas import ForecastListSchema
from src.forecast.services import ForecastService
from src.forecast.validators import validate_date

forecast_router = APIRouter(prefix="/weather")


@forecast_router.get(path="/current", response_model=CurrentForecastSchema)
@inject
async def get_current_weather(
    city: Annotated[str, Query(max_length=100)],
    forecast_service: Annotated[
        ForecastService, Depends(Provide[ForecastContainer.forecast_service])
    ],
) -> CurrentForecastSchema:
    response = await forecast_service.get_current_weather(city=city)

    return response


@forecast_router.get(path="/forecast", response_model=ForecastListSchema)
@inject
async def get_forecast(
    city: Annotated[str, Query(max_length=100)],
    date: Annotated[str, Depends(validate_date)],
    forecast_service: Annotated[
        ForecastService, Depends(Provide[ForecastContainer.forecast_service])
    ],
) -> ForecastListSchema:
    response = await forecast_service.get_forecast(city=city, date=date)

    return response


@forecast_router.post(path="/forecast", response_model=ForecastListSchema)
@inject
async def create_forecast(
    forecast: ForecastCreateSchema,
    forecast_service: Annotated[
        ForecastService, Depends(Provide[ForecastContainer.forecast_service])
    ],
) -> ForecastListSchema:
    response = await forecast_service.create(data=forecast)

    return response
