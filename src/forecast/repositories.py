import datetime

import httpx
from httpx import HTTPError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import HTTPRequestError
from src.forecast.models import Forecast
from src.forecast.schemas import CurrentWeatherAPIResponse
from src.forecast.schemas import ForecastCreateSchema
from src.forecast.schemas import ForecastWeatherAPIResponse


class ForecastRepository:
    async def get_by_city_and_date(
        self, session: AsyncSession, city: str, date: datetime.date
    ) -> Forecast | None:
        forecast = await session.scalar(
            select(Forecast)
            .where(Forecast.city == city.capitalize())
            .where(Forecast.date == date)
        )

        return forecast

    async def create(
        self, session: AsyncSession, data: ForecastCreateSchema
    ) -> Forecast:
        forecast_model = Forecast(**data.model_dump())

        session.add(forecast_model)
        await session.flush()

        return forecast_model


class APIForecastRepository:
    def __init__(self, weather_api_url: str, weather_api_key: str):
        self._weather_api_url = weather_api_url
        self._weather_api_key = weather_api_key

    async def get_current_weather(self, city: str) -> CurrentWeatherAPIResponse:
        url = (
            f"{self._weather_api_url}/current.json?q={city}&key={self._weather_api_key}"
        )

        try:
            async with httpx.AsyncClient() as client:
                raw_response = await client.get(url=url)
                raw_response.raise_for_status()
        except HTTPError:
            raise HTTPRequestError

        response = raw_response.json()

        return CurrentWeatherAPIResponse.model_validate(response)

    async def get_forecast(self, city: str, date: str) -> ForecastWeatherAPIResponse:
        days_cnt = (
            datetime.datetime.strptime(date, "%d.%m.%Y").date()
            - datetime.datetime.today().date()
        ).days + 1
        url = f"{self._weather_api_url}/forecast.json?q={city}&days={days_cnt}&key={self._weather_api_key}"

        try:
            async with httpx.AsyncClient() as client:
                raw_response = await client.get(url=url)
                raw_response.raise_for_status()
        except HTTPError:
            raise HTTPRequestError

        response = raw_response.json()

        return ForecastWeatherAPIResponse.model_validate(response)
