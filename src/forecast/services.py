import datetime
import logging

import pytz
from fastapi import HTTPException
from starlette import status

from src.database import SessionContextManager
from src.exceptions import HTTPRequestError
from src.forecast.repositories import APIForecastRepository
from src.forecast.repositories import ForecastRepository
from src.forecast.schemas import CurrentForecastSchema
from src.forecast.schemas import CurrentWeatherAPIResponse
from src.forecast.schemas import ForecastCreateSchema
from src.forecast.schemas import ForecastListSchema


class ForecastService:
    def __init__(
        self,
        api_forecast_repository: APIForecastRepository,
        forecast_repository: ForecastRepository,
        session_manager: SessionContextManager,
    ):
        self._api_forecast_repository = api_forecast_repository
        self._forecast_repository = forecast_repository
        self._session_manager = session_manager
        self._logger = logging.getLogger(__name__)

    async def get_current_weather(self, city: str) -> CurrentForecastSchema:
        try:
            response: CurrentWeatherAPIResponse = (
                await self._api_forecast_repository.get_current_weather(city=city)
            )
        except HTTPRequestError:
            self._logger.exception(msg="Ошибка при обращении к внешнему апи")
            raise HTTPException(
                detail="Ошибка при обращении к внешнему апи",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            local_time = datetime.datetime.fromtimestamp(
                response.current.last_updated_epoch,
                pytz.timezone(response.location.tz_id),
            ).strftime("%H:%M")
        except ValueError:
            self._logger.exception(msg="Ошибка при определении локального времени")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return CurrentForecastSchema(
            temperature=response.current.temp_c, local_time=local_time
        )

    async def create(self, data: ForecastCreateSchema) -> ForecastListSchema:
        async with self._session_manager as session, session.begin():
            forecast_model = await self._forecast_repository.create(
                session=session, data=data
            )

        return ForecastListSchema.model_validate(forecast_model)

    async def get_forecast(self, city: str, date: str) -> ForecastListSchema:
        async with self._session_manager as session, session.begin():
            forecast_model = await self._forecast_repository.get_by_city_and_date(
                session=session,
                city=city,
                date=datetime.datetime.strptime(date, "%d.%m.%Y"),
            )

            if forecast_model:
                return ForecastListSchema.model_validate(forecast_model)

        try:
            forecast_from_api = await self._api_forecast_repository.get_forecast(
                city=city, date=date
            )
        except HTTPRequestError:
            self._logger.exception(msg="Ошибка при обращении к внешнему апи")
            raise HTTPException(
                detail="Ошибка при обращении к внешнему апи",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        last_forecast = forecast_from_api.forecast.forecastday[-1]

        return ForecastListSchema(
            city=city,
            date=datetime.datetime.fromtimestamp(
                last_forecast.date_epoch,
                pytz.timezone(forecast_from_api.location.tz_id),
            ).date(),
            min_temperature=last_forecast.day.mintemp_c,
            max_temperature=last_forecast.day.maxtemp_c,
        )
