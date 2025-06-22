from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.containers import WiringConfiguration

from src.config.config import get_config
from src.database import SessionContextManager
from src.forecast.repositories import APIForecastRepository
from src.forecast.repositories import ForecastRepository
from src.forecast.services import ForecastService


class ForecastContainer(DeclarativeContainer):
    config = get_config()

    session_manager = providers.Dependency(instance_of=SessionContextManager)

    wiring_config = WiringConfiguration(modules=["src.forecast.router"])

    api_forecast_repository = providers.Factory(
        provides=APIForecastRepository,
        weather_api_url=config.weather_api.weather_api_url,
        weather_api_key=config.weather_api.openweather_api_key,
    )

    forecast_repository = providers.Factory(provides=ForecastRepository)

    forecast_service = providers.Factory(
        provides=ForecastService,
        api_forecast_repository=api_forecast_repository,
        forecast_repository=forecast_repository,
        session_manager=session_manager,
    )
